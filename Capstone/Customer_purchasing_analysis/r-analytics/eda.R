# eda.R: Exploratory Data Analysis, descriptive stats, correlations, distributions
source("utils.R")

get_eda_summary <- function(session_id) {
  dt <- load_session_data(session_id)
  
  # 1. Descriptive stats for numeric columns
  numeric_cols <- names(dt)[sapply(dt, is.numeric)]
  stats_list <- list()
  
  for (col in numeric_cols) {
    vals <- na.omit(dt[[col]])
    if (length(vals) > 0) {
      qs <- quantile(vals, probs = c(0.25, 0.5, 0.75), na.rm = TRUE)
      stats_list[[col]] <- list(
        column = col,
        count = length(vals),
        mean = round(mean(vals), 2),
        std_dev = round(sd(vals), 2),
        min = round(min(vals), 2),
        q25 = round(unname(qs[1]), 2),
        median = round(unname(qs[2]), 2),
        q75 = round(unname(qs[3]), 2),
        max = round(max(vals), 2),
        missing = sum(is.na(dt[[col]]))
      )
    }
  }
  
  # 2. Key distributions (histogram bins)
  distributions <- list()
  dist_cols <- intersect(c("time_on_page_seconds", "cart_value", "purchase_amount", 
                           "session_page_number", "customer_lifetime_value"), numeric_cols)
  for (col in dist_cols) {
    vals <- na.omit(dt[[col]])
    if (length(vals) > 20) {
      # Filter zeroes for purchase_amount or cart_value for better histogram visualization
      if (col %in% c("purchase_amount", "cart_value")) {
        vals <- vals[vals > 0]
      }
      if (length(vals) > 10) {
        h <- hist(vals, breaks = 20, plot = FALSE)
        distributions[[col]] <- list(
          column = col,
          bins = lapply(1:(length(h$breaks)-1), function(i) {
            paste0(round(h$breaks[i], 1), " - ", round(h$breaks[i+1], 1))
          }),
          counts = as.list(h$counts)
        )
      }
    }
  }
  
  # 3. Correlation matrix for key numeric columns
  cor_cols <- intersect(c(
    "product_price", "session_page_number", "time_on_page_seconds", 
    "cart_value", "purchase_amount", "session_converted", "customer_lifetime_value",
    "previous_purchase_count", "historical_average_order_value", "customer_tenure_days"
  ), numeric_cols)
  
  cor_matrix <- list()
  if (length(cor_cols) >= 2) {
    sub_dt <- na.omit(dt[, ..cor_cols])
    if (nrow(sub_dt) > 10) {
      c_mat <- cor(sub_dt, use = "pairwise.complete.obs")
      # Format for ECharts heatmap: [i, j, value]
      cor_items <- list()
      for (i in 1:length(cor_cols)) {
        for (j in 1:length(cor_cols)) {
          val <- round(c_mat[i, j], 3)
          cor_items[[length(cor_items) + 1]] <- list(
            x = cor_cols[i],
            y = cor_cols[j],
            x_idx = i - 1,
            y_idx = j - 1,
            value = ifelse(is.na(val), 0, val)
          )
        }
      }
      cor_matrix <- list(
        columns = cor_cols,
        items = cor_items
      )
    }
  }
  
  # 4. Categorical frequencies
  cat_cols <- intersect(c("device_type", "traffic_source", "visitor_type", 
                        "browser", "country", "customer_segment", "event_type"), names(dt))
  cat_frequencies <- list()
  for (col in cat_cols) {
    counts <- dt[, .N, by = col][order(-N)]
    names(counts) <- c("category", "count")
    cat_frequencies[[col]] <- lapply(1:min(12, nrow(counts)), function(i) {
      list(name = as.character(counts$category[i]), count = as.integer(counts$count[i]))
    })
  }
  
  # 5. Device & Traffic Conversion Analysis
  device_conv <- list()
  if (all(c("device_type", "session_id", "session_converted") %in% names(dt))) {
    d_dt <- dt[, .(conv = max(session_converted, na.rm = TRUE)), by = .(session_id, device_type)]
    d_agg <- d_dt[, .(sessions = .N, conversions = sum(conv == 1, na.rm = TRUE)), by = device_type]
    d_agg[, rate := round((conversions / sessions) * 100, 2)]
    device_conv <- lapply(1:nrow(d_agg), function(i) {
      list(
        device = as.character(d_agg$device_type[i]),
        sessions = as.integer(d_agg$sessions[i]),
        conversions = as.integer(d_agg$conversions[i]),
        rate = as.numeric(d_agg$rate[i])
      )
    })
  }
  
  traffic_conv <- list()
  if (all(c("traffic_source", "session_id", "session_converted") %in% names(dt))) {
    t_dt <- dt[, .(conv = max(session_converted, na.rm = TRUE)), by = .(session_id, traffic_source)]
    t_agg <- t_dt[, .(sessions = .N, conversions = sum(conv == 1, na.rm = TRUE)), by = traffic_source]
    t_agg[, rate := round((conversions / sessions) * 100, 2)]
    traffic_conv <- lapply(1:nrow(t_agg), function(i) {
      list(
        source = as.character(t_agg$traffic_source[i]),
        sessions = as.integer(t_agg$sessions[i]),
        conversions = as.integer(t_agg$conversions[i]),
        rate = as.numeric(t_agg$rate[i])
      )
    })
  }
  
  return(list(
    numeric_stats = unname(stats_list),
    distributions = distributions,
    correlations = cor_matrix,
    categoricals = cat_frequencies,
    device_conversion = device_conv,
    traffic_conversion = traffic_conv
  ))
}
