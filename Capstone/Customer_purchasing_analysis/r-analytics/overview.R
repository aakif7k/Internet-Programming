# overview.R: Dataset summary KPIs and high-level health
source("utils.R")

get_overview_kpis <- function(session_id) {
  dt <- load_session_data(session_id)
  ds_info <- get_active_dataset_path(session_id)
  
  # Total events
  total_events <- nrow(dt)
  
  # Sessions & Customers
  has_session_col <- "session_id" %in% names(dt)
  has_customer_col <- "customer_id" %in% names(dt)
  total_sessions <- if (has_session_col) data.table::uniqueN(dt$session_id) else total_events
  total_customers <- if (has_customer_col) data.table::uniqueN(dt$customer_id) else total_sessions
  
  # Conversions & Revenue
  # Converted sessions: either session_converted == 1 or has purchase event
  converted_sessions <- 0
  total_revenue <- 0
  
  if (has_session_col) {
    if ("session_converted" %in% names(dt)) {
      sess_conv <- dt[, .(conv = max(session_converted, na.rm = TRUE)), by = session_id]
      converted_sessions <- sum(sess_conv$conv == 1, na.rm = TRUE)
    } else if ("event_type" %in% names(dt)) {
      sess_conv <- dt[, .(conv = as.integer(any(event_type == "purchase" | event_type == "checkout"))), by = session_id]
      converted_sessions <- sum(sess_conv$conv == 1, na.rm = TRUE)
    }
    
    if ("purchase_amount" %in% names(dt)) {
      # Sum positive purchase amounts
      if ("event_type" %in% names(dt)) {
        purch_rows <- dt[event_type == "purchase" & purchase_amount > 0]
        if (nrow(purch_rows) > 0) {
          total_revenue <- sum(purch_rows$purchase_amount, na.rm = TRUE)
        } else {
          sess_rev <- dt[, .(rev = max(purchase_amount, na.rm = TRUE)), by = session_id]
          total_revenue <- sum(sess_rev$rev[sess_rev$rev > 0], na.rm = TRUE)
        }
      } else {
        sess_rev <- dt[, .(rev = max(purchase_amount, na.rm = TRUE)), by = session_id]
        total_revenue <- sum(sess_rev$rev[sess_rev$rev > 0], na.rm = TRUE)
      }
    }
  }
  
  conversion_rate <- if (total_sessions > 0) round((converted_sessions / total_sessions) * 100, 2) else 0
  aov <- if (converted_sessions > 0) round(total_revenue / converted_sessions, 2) else 0
  
  # Event types breakdown
  event_breakdown <- list()
  if ("event_type" %in% names(dt)) {
    ev_counts <- dt[, .N, by = event_type][order(-N)]
    event_breakdown <- lapply(1:nrow(ev_counts), function(i) {
      list(name = as.character(ev_counts$event_type[i]), count = as.integer(ev_counts$N[i]))
    })
  }
  
  # Device breakdown
  device_breakdown <- list()
  if ("device_type" %in% names(dt)) {
    dev_counts <- dt[, .(events = .N, sessions = if (has_session_col) data.table::uniqueN(session_id) else .N), by = device_type][order(-events)]
    device_breakdown <- lapply(1:nrow(dev_counts), function(i) {
      list(name = as.character(dev_counts$device_type[i]), events = as.integer(dev_counts$events[i]), sessions = as.integer(dev_counts$sessions[i]))
    })
  }
  
  # Traffic breakdown
  traffic_breakdown <- list()
  if ("traffic_source" %in% names(dt)) {
    tr_counts <- dt[, .(events = .N, sessions = if (has_session_col) data.table::uniqueN(session_id) else .N), by = traffic_source][order(-events)]
    traffic_breakdown <- lapply(1:nrow(tr_counts), function(i) {
      list(name = as.character(tr_counts$traffic_source[i]), events = as.integer(tr_counts$events[i]), sessions = as.integer(tr_counts$sessions[i]))
    })
  }
  
  # Sparkline daily activity (last 14-30 days available)
  daily_trend <- list()
  if ("event_timestamp" %in% names(dt) && any(!is.na(dt$event_timestamp))) {
    dt[, event_date := as.character(as.Date(event_timestamp))]
    day_counts <- dt[!is.na(event_date), .(
      events = .N, 
      sessions = if (has_session_col) data.table::uniqueN(session_id) else .N,
      revenue = if ("purchase_amount" %in% names(dt)) sum(purchase_amount[event_type == "purchase"], na.rm = TRUE) else 0
    ), by = event_date][order(event_date)]
    
    daily_trend <- lapply(1:nrow(day_counts), function(i) {
      list(
        date = day_counts$event_date[i],
        events = as.integer(day_counts$events[i]),
        sessions = as.integer(day_counts$sessions[i]),
        revenue = round(as.numeric(day_counts$revenue[i]), 2)
      )
    })
  }
  
  return(list(
    dataset_status = ds_info$type,
    total_events = total_events,
    total_sessions = total_sessions,
    total_customers = total_customers,
    converted_sessions = converted_sessions,
    conversion_rate = conversion_rate,
    total_revenue = round(total_revenue, 2),
    avg_order_value = aov,
    event_breakdown = event_breakdown,
    device_breakdown = device_breakdown,
    traffic_breakdown = traffic_breakdown,
    daily_trend = daily_trend
  ))
}
