# purchase_patterns.R: Analysis of viewed vs purchased products, AOV, time patterns
source("utils.R")

get_purchase_patterns <- function(session_id) {
  dt <- load_session_data(session_id)
  check_required_columns(dt, c("session_id", "event_type"))
  
  # 1. Top Viewed vs Purchased Categories
  cat_comparison <- list()
  if ("product_category" %in% names(dt)) {
    valid_cats <- dt[product_category != "" & !is.na(product_category) & product_category != "Unknown"]
    if (nrow(valid_cats) > 0) {
      views <- valid_cats[event_type %in% c("product_view", "category_view"), .(views = .N), by = product_category]
      purchases <- valid_cats[event_type == "purchase" | (is_conversion_event == 1), .(
        purchases = .N,
        revenue = if ("purchase_amount" %in% names(valid_cats)) sum(purchase_amount, na.rm = TRUE) else 0
      ), by = product_category]
      
      merged_cats <- merge(views, purchases, by = "product_category", all = TRUE)
      merged_cats[is.na(views), views := 0]
      merged_cats[is.na(purchases), purchases := 0]
      merged_cats[is.na(revenue), revenue := 0]
      merged_cats[, conv_ratio := round((purchases / pmax(views, 1)) * 100, 2)]
      data.table::setorder(merged_cats, -revenue)
      
      top_cats <- head(merged_cats, 10)
      cat_comparison <- lapply(1:nrow(top_cats), function(i) {
        list(
          category = as.character(top_cats$product_category[i]),
          views = as.integer(top_cats$views[i]),
          purchases = as.integer(top_cats$purchases[i]),
          revenue = round(as.numeric(top_cats$revenue[i]), 2),
          conversion_ratio = as.numeric(top_cats$conv_ratio[i])
        )
      })
    }
  }
  
  # 2. Top Viewed vs Purchased Products
  prod_comparison <- list()
  if ("product_name" %in% names(dt)) {
    valid_prods <- dt[product_name != "" & !is.na(product_name) & product_name != "Unknown"]
    if (nrow(valid_prods) > 0) {
      p_views <- valid_prods[event_type == "product_view", .(views = .N), by = product_name]
      p_purch <- valid_prods[event_type == "purchase" | (is_conversion_event == 1), .(
        purchases = .N,
        revenue = if ("purchase_amount" %in% names(valid_prods)) sum(purchase_amount, na.rm = TRUE) else 0
      ), by = product_name]
      
      m_prods <- merge(p_views, p_purch, by = "product_name", all = TRUE)
      m_prods[is.na(views), views := 0]
      m_prods[is.na(purchases), purchases := 0]
      m_prods[is.na(revenue), revenue := 0]
      data.table::setorder(m_prods, -revenue)
      
      top_prods <- head(m_prods, 10)
      prod_comparison <- lapply(1:nrow(top_prods), function(i) {
        list(
          product = as.character(top_prods$product_name[i]),
          views = as.integer(top_prods$views[i]),
          purchases = as.integer(top_prods$purchases[i]),
          revenue = round(as.numeric(top_prods$revenue[i]), 2)
        )
      })
    }
  }
  
  # 3. Average Order Value (AOV) by Dimensions
  aov_by_device <- list()
  if (all(c("device_type", "purchase_amount") %in% names(dt))) {
    p_dev <- dt[(event_type == "purchase" | is_conversion_event == 1) & purchase_amount > 0, .(
      orders = .N,
      revenue = sum(purchase_amount, na.rm = TRUE),
      aov = round(mean(purchase_amount, na.rm = TRUE), 2)
    ), by = device_type]
    aov_by_device <- lapply(1:nrow(p_dev), function(i) {
      list(
        dimension = as.character(p_dev$device_type[i]),
        orders = as.integer(p_dev$orders[i]),
        revenue = round(as.numeric(p_dev$revenue[i]), 2),
        aov = as.numeric(p_dev$aov[i])
      )
    })
  }
  
  aov_by_traffic <- list()
  if (all(c("traffic_source", "purchase_amount") %in% names(dt))) {
    p_tr <- dt[(event_type == "purchase" | is_conversion_event == 1) & purchase_amount > 0, .(
      orders = .N,
      revenue = sum(purchase_amount, na.rm = TRUE),
      aov = round(mean(purchase_amount, na.rm = TRUE), 2)
    ), by = traffic_source]
    aov_by_traffic <- lapply(1:nrow(p_tr), function(i) {
      list(
        dimension = as.character(p_tr$traffic_source[i]),
        orders = as.integer(p_tr$orders[i]),
        revenue = round(as.numeric(p_tr$revenue[i]), 2),
        aov = as.numeric(p_tr$aov[i])
      )
    })
  }
  
  # 4. Hourly and Day of Week Purchase Patterns
  hourly_purchases <- list()
  dow_purchases <- list()
  
  # Try session_hour or event_timestamp
  if ("session_hour" %in% names(dt) && "purchase_amount" %in% names(dt)) {
    h_agg <- dt[(event_type == "purchase" | is_conversion_event == 1) & purchase_amount > 0, .(
      orders = .N,
      revenue = sum(purchase_amount, na.rm = TRUE)
    ), by = session_hour][order(session_hour)]
    hourly_purchases <- lapply(1:nrow(h_agg), function(i) {
      list(hour = as.integer(h_agg$session_hour[i]), orders = as.integer(h_agg$orders[i]), revenue = round(as.numeric(h_agg$revenue[i]), 2))
    })
  } else if ("event_timestamp" %in% names(dt) && "purchase_amount" %in% names(dt)) {
    dt_time <- dt[!is.na(event_timestamp) & (event_type == "purchase" | is_conversion_event == 1)]
    if (nrow(dt_time) > 0) {
      dt_time[, hour := as.integer(format(event_timestamp, "%H"))]
      h_agg <- dt_time[, .(orders = .N, revenue = sum(purchase_amount, na.rm = TRUE)), by = hour][order(hour)]
      hourly_purchases <- lapply(1:nrow(h_agg), function(i) {
        list(hour = as.integer(h_agg$hour[i]), orders = as.integer(h_agg$orders[i]), revenue = round(as.numeric(h_agg$revenue[i]), 2))
      })
    }
  }
  
  if ("day_of_week" %in% names(dt) && "purchase_amount" %in% names(dt)) {
    d_order <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    d_agg <- dt[(event_type == "purchase" | is_conversion_event == 1) & purchase_amount > 0, .(
      orders = .N,
      revenue = sum(purchase_amount, na.rm = TRUE)
    ), by = day_of_week]
    # order by day of week
    d_agg$day_factor <- factor(d_agg$day_of_week, levels = d_order)
    data.table::setorder(d_agg, day_factor)
    dow_purchases <- lapply(1:nrow(d_agg), function(i) {
      list(day = as.character(d_agg$day_of_week[i]), orders = as.integer(d_agg$orders[i]), revenue = round(as.numeric(d_agg$revenue[i]), 2))
    })
  }
  
  return(list(
    categories = cat_comparison,
    products = prod_comparison,
    aov_by_device = aov_by_device,
    aov_by_traffic = aov_by_traffic,
    hourly = hourly_purchases,
    day_of_week = dow_purchases
  ))
}
