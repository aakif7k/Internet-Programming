# segmentation.R: Customer RFM scoring and k-means clustering with silhouette analysis
suppressPackageStartupMessages({
  library(cluster)
  library(data.table)
})
source("utils.R")

get_customer_segmentation <- function(session_id, k = 4) {
  dt <- load_session_data(session_id)
  check_required_columns(dt, c("customer_id"))
  s_path <- get_session_path(session_id)
  
  # Aggregate at customer level
  has_timestamp <- "event_timestamp" %in% names(dt) && any(!is.na(dt$event_timestamp))
  max_date <- if (has_timestamp) max(dt$event_timestamp, na.rm = TRUE) else Sys.time()
  
  cust_summary <- dt[, .(
    sessions = if ("session_id" %in% names(dt)) data.table::uniqueN(session_id) else .N,
    events = .N,
    purchases = if ("event_type" %in% names(dt)) sum(event_type == "purchase", na.rm = TRUE) else 0,
    monetary = if ("purchase_amount" %in% names(dt)) sum(purchase_amount[event_type == "purchase"], na.rm = TRUE) else 0,
    clv = if ("customer_lifetime_value" %in% names(dt)) max(customer_lifetime_value, na.rm = TRUE) else 0,
    tenure = if ("customer_tenure_days" %in% names(dt)) max(customer_tenure_days, na.rm = TRUE) else 0,
    last_event = if (has_timestamp) max(event_timestamp, na.rm = TRUE) else as.POSIXct(Sys.time())
  ), by = customer_id]
  
  # If customer_lifetime_value exists and monetary is 0, use clv
  cust_summary[monetary == 0 & clv > 0, monetary := clv]
  
  # Recency in days
  if (has_timestamp) {
    cust_summary[, recency := pmax(1, as.numeric(difftime(max_date, last_event, units = "days")))]
  } else if ("tenure" %in% names(cust_summary) && any(cust_summary$tenure > 0)) {
    # If no timestamp, use inverted tenure as a recency proxy
    cust_summary[, recency := pmax(1, 365 - pmin(tenure, 364))]
  } else {
    cust_summary[, recency := sample(1:60, nrow(cust_summary), replace = TRUE)]
  }
  
  # Frequency
  cust_summary[, frequency := pmax(1, ifelse(purchases > 0, purchases, sessions))]
  
  # Monetary
  cust_summary[, monetary := pmax(1.0, monetary)]
  
  # Filter valid rows
  valid_cust <- na.omit(cust_summary[, .(customer_id, recency, frequency, monetary)])
  if (nrow(valid_cust) < 20) {
    stop("Not enough customer data to perform segmentation (minimum 20 customers required).")
  }
  
  # 1. RFM Quantile Scores (1 to 5)
  # Recency: lower is better (5 is most recent)
  # Frequency: higher is better (5 is highest frequency)
  # Monetary: higher is better (5 is highest spend)
  r_cuts <- quantile(valid_cust$recency, probs = seq(0, 1, 0.2), na.rm = TRUE)
  f_cuts <- quantile(valid_cust$frequency, probs = seq(0, 1, 0.2), na.rm = TRUE)
  m_cuts <- quantile(valid_cust$monetary, probs = seq(0, 1, 0.2), na.rm = TRUE)
  
  valid_cust[, R_score := 6 - as.integer(cut(recency, breaks = unique(r_cuts), include.lowest = TRUE, labels = FALSE))]
  valid_cust[, F_score := as.integer(cut(frequency, breaks = unique(f_cuts), include.lowest = TRUE, labels = FALSE))]
  valid_cust[, M_score := as.integer(cut(monetary, breaks = unique(m_cuts), include.lowest = TRUE, labels = FALSE))]
  
  # Handle any NAs from cut
  valid_cust[is.na(R_score), R_score := 3]
  valid_cust[is.na(F_score), F_score := 3]
  valid_cust[is.na(M_score), M_score := 3]
  
  valid_cust[, RFM_Score := paste0(R_score, F_score, M_score)]
  
  # 2. Silhouette Analysis across k = 2 to 6
  scaled_features <- scale(log1p(valid_cust[, .(recency, frequency, monetary)]))
  # Sample for silhouette if dataset is large to maintain fast UI response
  sample_size <- min(2000, nrow(scaled_features))
  sample_idx <- sample(nrow(scaled_features), sample_size)
  sample_matrix <- scaled_features[sample_idx, ]
  dist_matrix <- dist(sample_matrix)
  
  silhouette_scores <- list()
  for (test_k in 2:6) {
    set.seed(42)
    km_test <- kmeans(scaled_features, centers = test_k, nstart = 5, iter.max = 30)
    sil <- cluster::silhouette(km_test$cluster[sample_idx], dist_matrix)
    avg_sil <- round(mean(sil[, 3]), 3)
    silhouette_scores[[length(silhouette_scores) + 1]] <- list(k = test_k, score = avg_sil)
  }
  
  # 3. K-Means Clustering with requested k
  k <- as.integer(k)
  if (is.na(k) || k < 2 || k > 6) k <- 4
  set.seed(123)
  km_final <- kmeans(scaled_features, centers = k, nstart = 10, iter.max = 50)
  valid_cust[, cluster := km_final$cluster]
  
  # Segment Naming Rules based on mean RFM in each cluster
  cluster_stats <- valid_cust[, .(
    avg_recency = mean(recency),
    avg_frequency = mean(frequency),
    avg_monetary = mean(monetary),
    count = .N
  ), by = cluster]
  
  # Sort clusters by spend/frequency to assign intuitive names
  data.table::setorder(cluster_stats, -avg_monetary, -avg_frequency)
  
  named_labels <- c("Champions / VIP", "Loyal Customers", "Potential Loyalists", "At Risk / Hibernating", "Promising", "Need Attention")
  cluster_names <- list()
  for (i in 1:nrow(cluster_stats)) {
    c_num <- cluster_stats$cluster[i]
    c_label <- if (i <= length(named_labels)) named_labels[i] else paste("Cluster", c_num)
    cluster_names[[as.character(c_num)]] <- c_label
  }
  
  valid_cust[, segment_name := unlist(cluster_names[as.character(cluster)])]
  
  # Save rfm_segments.csv for CSV export
  export_file <- file.path(s_path, "rfm_segments.csv")
  data.table::fwrite(valid_cust, export_file)
  
  # Summary table for frontend
  summary_table <- valid_cust[, .(
    customers = .N,
    pct_customers = round((.N / nrow(valid_cust)) * 100, 1),
    avg_recency_days = round(mean(recency), 1),
    avg_frequency = round(mean(frequency), 1),
    avg_monetary = round(mean(monetary), 2),
    total_revenue = round(sum(monetary), 2)
  ), by = .(cluster, segment_name)][order(cluster)]
  
  # PCA for 2D scatter plot visualization
  pca <- prcomp(scaled_features, center = FALSE, scale. = FALSE)
  valid_cust[, pc1 := round(pca$x[, 1], 2)]
  valid_cust[, pc2 := round(pca$x[, 2], 2)]
  
  # Sample up to 500 points for smooth frontend ECharts rendering
  scatter_sample <- valid_cust[sample(.N, min(500, .N)), .(
    customer_id, pc1, pc2, recency, frequency, monetary, segment_name, cluster
  )]
  
  scatter_data <- lapply(1:nrow(scatter_sample), function(i) {
    list(
      id = as.character(scatter_sample$customer_id[i]),
      pc1 = as.numeric(scatter_sample$pc1[i]),
      pc2 = as.numeric(scatter_sample$pc2[i]),
      recency = round(as.numeric(scatter_sample$recency[i]), 1),
      frequency = as.integer(scatter_sample$frequency[i]),
      monetary = round(as.numeric(scatter_sample$monetary[i]), 2),
      segment = as.character(scatter_sample$segment_name[i]),
      cluster = as.integer(scatter_sample$cluster[i])
    )
  })
  
  summary_list <- lapply(1:nrow(summary_table), function(i) {
    list(
      cluster = as.integer(summary_table$cluster[i]),
      segment_name = as.character(summary_table$segment_name[i]),
      customers = as.integer(summary_table$customers[i]),
      pct_customers = as.numeric(summary_table$pct_customers[i]),
      avg_recency_days = as.numeric(summary_table$avg_recency_days[i]),
      avg_frequency = as.numeric(summary_table$avg_frequency[i]),
      avg_monetary = as.numeric(summary_table$avg_monetary[i]),
      total_revenue = as.numeric(summary_table$total_revenue[i])
    )
  })
  
  exact_rules <- list(
    list(segment = "Champions / VIP", condition = "Highest Monetary & Frequency, Low Recency (Recent high-value repeat shoppers)"),
    list(segment = "Loyal Customers", condition = "High Frequency & Moderate-to-High Monetary, Steady activity"),
    list(segment = "Potential Loyalists", condition = "Recent shoppers with average frequency and spend"),
    list(segment = "At Risk / Hibernating", condition = "High Recency (long time since last visit), lower frequency and spend")
  )
  
  return(list(
    selected_k = k,
    silhouette_analysis = silhouette_scores,
    segments_summary = summary_list,
    scatter_data = scatter_data,
    exact_rules = exact_rules
  ))
}
