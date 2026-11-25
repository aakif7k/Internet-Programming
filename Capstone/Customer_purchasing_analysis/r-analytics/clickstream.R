# clickstream.R: Clickstream navigation paths, transitions, and page engagement
source("utils.R")

get_clickstream_analysis <- function(session_id) {
  dt <- load_session_data(session_id)
  
  # 1. Event Counts
  check_required_columns(dt, c("event_type", "session_id"))
  
  event_counts <- dt[, .(
    count = .N,
    sessions = data.table::uniqueN(session_id),
    avg_time_sec = if ("time_on_page_seconds" %in% names(dt)) round(mean(time_on_page_seconds, na.rm = TRUE), 1) else 0
  ), by = event_type][order(-count)]
  
  event_summary <- lapply(1:nrow(event_counts), function(i) {
    list(
      event_type = as.character(event_counts$event_type[i]),
      count = as.integer(event_counts$count[i]),
      sessions = as.integer(event_counts$sessions[i]),
      avg_time_sec = as.numeric(event_counts$avg_time_sec[i])
    )
  })
  
  # 2. Most Visited Pages
  page_summary <- list()
  if ("page_url" %in% names(dt)) {
    pg_counts <- dt[page_url != "" & !is.na(page_url), .(
      views = .N,
      unique_sessions = data.table::uniqueN(session_id),
      avg_time = if ("time_on_page_seconds" %in% names(dt)) round(mean(time_on_page_seconds, na.rm = TRUE), 1) else 0
    ), by = page_url][order(-views)][1:min(15, .N)]
    
    page_summary <- lapply(1:nrow(pg_counts), function(i) {
      list(
        page_url = as.character(pg_counts$page_url[i]),
        views = as.integer(pg_counts$views[i]),
        unique_sessions = as.integer(pg_counts$unique_sessions[i]),
        avg_time = as.numeric(pg_counts$avg_time[i])
      )
    })
  }
  
  # 3. Top Navigation Paths (first 3-4 steps in session)
  paths_summary <- list()
  order_col <- if ("session_page_number" %in% names(dt)) "session_page_number" else if ("event_timestamp" %in% names(dt)) "event_timestamp" else NULL
  
  if (!is.null(order_col)) {
    data.table::setorderv(dt, c("session_id", order_col))
    # Aggregate top 3-4 events per session
    sess_paths <- dt[, .(path = paste(head(event_type, 4), collapse = " -> ")), by = session_id]
    top_paths <- sess_paths[, .N, by = path][order(-N)][1:min(10, .N)]
    
    paths_summary <- lapply(1:nrow(top_paths), function(i) {
      list(
        path = as.character(top_paths$path[i]),
        count = as.integer(top_paths$N[i]),
        pct = round((top_paths$N[i] / data.table::uniqueN(dt$session_id)) * 100, 2)
      )
    })
  }
  
  # 4. Event Transition Matrix (Markov transition probabilities between sequential events)
  transitions <- list()
  if (!is.null(order_col)) {
    dt_seq <- dt[, .(
      from_event = head(event_type, -1),
      to_event = tail(event_type, -1)
    ), by = session_id]
    
    if (nrow(dt_seq) > 0) {
      tr_counts <- dt_seq[, .N, by = .(from_event, to_event)]
      # Calculate transition probabilities
      tr_counts[, total_from := sum(N), by = from_event]
      tr_counts[, prob := round(N / total_from, 3)]
      
      unique_events <- unique(c(tr_counts$from_event, tr_counts$to_event))
      
      tr_items <- lapply(1:nrow(tr_counts), function(i) {
        list(
          source = as.character(tr_counts$from_event[i]),
          target = as.character(tr_counts$to_event[i]),
          count = as.integer(tr_counts$N[i]),
          probability = as.numeric(tr_counts$prob[i])
        )
      })
      
      transitions <- list(
        events = unique_events,
        links = tr_items
      )
    }
  }
  
  # 5. Session Engagement & Bounce Rate
  # Bounce = session with only 1 event
  sess_len <- dt[, .N, by = session_id]
  bounce_count <- sum(sess_len$N == 1)
  bounce_rate <- round((bounce_count / nrow(sess_len)) * 100, 2)
  avg_events_per_session <- round(mean(sess_len$N), 2)
  
  return(list(
    events = event_summary,
    pages = page_summary,
    top_paths = paths_summary,
    transitions = transitions,
    engagement = list(
      bounce_count = bounce_count,
      bounce_rate = bounce_rate,
      avg_events_per_session = avg_events_per_session
    )
  ))
}
