# time_series.R: Time-series aggregations and forecasting with forecast package (ETS & ARIMA)
suppressPackageStartupMessages({
  library(data.table)
  library(forecast)
})
source("utils.R")

get_time_series_data <- function(session_id, metric = "revenue", interval = "daily", forecast_periods = 14) {
  dt <- load_session_data(session_id)
  check_required_columns(dt, c("event_timestamp"))
  
  # Filter valid timestamps
  dt_ts <- dt[!is.na(event_timestamp)]
  if (nrow(dt_ts) == 0) {
    stop("No valid timestamps found for time-series analysis.")
  }
  
  # Format period key
  if (interval == "weekly") {
    dt_ts[, period := format(as.Date(cut(as.Date(event_timestamp), "week")), "%Y-%m-%d")]
  } else if (interval == "monthly") {
    dt_ts[, period := format(as.Date(event_timestamp), "%Y-%m-01")]
  } else {
    # Default daily
    dt_ts[, period := format(as.Date(event_timestamp), "%Y-%m-%d")]
  }
  
  # Aggregate metrics per period
  ts_agg <- dt_ts[, .(
    events = .N,
    sessions = if ("session_id" %in% names(dt_ts)) data.table::uniqueN(session_id) else .N,
    conversions = if ("session_converted" %in% names(dt_ts)) sum(session_converted == 1, na.rm = TRUE) 
                  else if ("event_type" %in% names(dt_ts)) sum(event_type == "purchase", na.rm = TRUE) else 0,
    revenue = if ("purchase_amount" %in% names(dt_ts)) sum(purchase_amount[event_type == "purchase" | is_conversion_event == 1], na.rm = TRUE) else 0
  ), by = period][order(period)]
  
  # Conversion rate per period
  ts_agg[, conversion_rate := round((conversions / pmax(sessions, 1)) * 100, 2)]
  ts_agg[, revenue := round(revenue, 2)]
  
  # Ensure historical series is long enough for forecasting
  periods <- ts_agg$period
  y_vals <- switch(metric,
    "revenue" = ts_agg$revenue,
    "sessions" = ts_agg$sessions,
    "conversions" = ts_agg$conversions,
    "conversion_rate" = ts_agg$conversion_rate,
    ts_agg$revenue
  )
  
  forecast_results <- list()
  if (length(y_vals) >= 7) {
    # Fit ARIMA model using forecast package
    y_ts <- ts(y_vals, frequency = if (interval == "daily") 7 else if (interval == "monthly") 12 else 4)
    fit_arima <- tryCatch({
      forecast::auto.arima(y_ts)
    }, error = function(e) {
      forecast::ets(y_ts)
    })
    
    fc <- forecast::forecast(fit_arima, h = as.integer(forecast_periods))
    
    # Generate future dates
    last_date <- as.Date(tail(periods, 1))
    step_days <- if (interval == "weekly") 7 else if (interval == "monthly") 30 else 1
    future_dates <- as.character(last_date + seq(step_days, step_days * as.integer(forecast_periods), by = step_days))
    
    forecast_results <- lapply(1:length(fc$mean), function(i) {
      list(
        period = future_dates[i],
        forecast = round(max(0, as.numeric(fc$mean[i])), 2),
        lower_80 = round(max(0, as.numeric(fc$lower[i, 1])), 2),
        upper_80 = round(max(0, as.numeric(fc$upper[i, 1])), 2),
        lower_95 = round(max(0, as.numeric(fc$lower[i, 2])), 2),
        upper_95 = round(max(0, as.numeric(fc$upper[i, 2])), 2)
      )
    })
  }
  
  historical_data <- lapply(1:nrow(ts_agg), function(i) {
    list(
      period = as.character(ts_agg$period[i]),
      events = as.integer(ts_agg$events[i]),
      sessions = as.integer(ts_agg$sessions[i]),
      conversions = as.integer(ts_agg$conversions[i]),
      revenue = as.numeric(ts_agg$revenue[i]),
      conversion_rate = as.numeric(ts_agg$conversion_rate[i])
    )
  })
  
  return(list(
    metric = metric,
    interval = interval,
    total_periods = nrow(ts_agg),
    historical = historical_data,
    forecast = forecast_results
  ))
}
