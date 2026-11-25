# funnel.R: Configurable conversion funnel analysis
source("utils.R")

get_funnel_analysis <- function(session_id, stages = NULL) {
  dt <- load_session_data(session_id)
  check_required_columns(dt, c("session_id", "event_type"))
  
  # Default stages: Home/Browse -> Add to Cart -> Checkout -> Purchase
  if (is.null(stages) || length(stages) == 0) {
    stages <- list(
      list(name = "Browsing", events = c("home", "category_view", "product_view", "search")),
      list(name = "Add to Cart", events = c("add_to_cart")),
      list(name = "Checkout", events = c("checkout")),
      list(name = "Purchase", events = c("purchase"))
    )
  }
  
  # Unique sessions per stage
  stage_results <- list()
  previous_sessions <- NULL
  total_entry_sessions <- 0
  
  for (i in 1:length(stages)) {
    stage_def <- stages[[i]]
    stage_name <- stage_def$name
    stage_events <- stage_def$events
    
    # Sessions that had any of these events
    matching_sessions <- unique(dt[event_type %in% stage_events, session_id])
    
    # Enforce sequential funnel progression: session must have been in previous stage
    if (i == 1) {
      qualified_sessions <- matching_sessions
      total_entry_sessions <- length(qualified_sessions)
    } else {
      qualified_sessions <- intersect(previous_sessions, matching_sessions)
    }
    
    stage_count <- length(qualified_sessions)
    previous_count <- if (i == 1) stage_count else length(previous_sessions)
    
    drop_off_count <- if (i == 1) 0 else max(0, previous_count - stage_count)
    drop_off_rate <- if (previous_count > 0 && i > 1) round((drop_off_count / previous_count) * 100, 2) else 0
    step_conversion <- if (previous_count > 0 && i > 1) round((stage_count / previous_count) * 100, 2) else 100
    overall_conversion <- if (total_entry_sessions > 0) round((stage_count / total_entry_sessions) * 100, 2) else 0
    
    stage_results[[i]] <- list(
      step = i,
      name = stage_name,
      events = stage_events,
      sessions = stage_count,
      drop_off_count = drop_off_count,
      drop_off_rate = drop_off_rate,
      step_conversion = step_conversion,
      overall_conversion = overall_conversion
    )
    
    previous_sessions <- qualified_sessions
  }
  
  # Available distinct event types for frontend stage customization
  available_events <- sort(unique(dt$event_type))
  
  return(list(
    total_entry_sessions = total_entry_sessions,
    overall_funnel_rate = if (length(stage_results) > 0) stage_results[[length(stage_results)]]$overall_conversion else 0,
    stages = stage_results,
    available_events = available_events
  ))
}
