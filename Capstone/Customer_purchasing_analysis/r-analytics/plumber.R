# plumber.R: Main Plumber API router for R Analytics
suppressPackageStartupMessages({
  library(plumber)
  library(jsonlite)
})

# Source module files
source("utils.R")
source("overview.R")
source("preprocessing.R")
source("eda.R")
source("clickstream.R")
source("purchase_patterns.R")
source("funnel.R")
source("segmentation.R")
source("conversion_prediction.R")
source("revenue_estimation.R")
source("time_series.R")
source("visual_studio.R")

# Helper to reliably extract session_id as a single string scalar
extract_sid <- function(req, session_id = "") {
  # 1. From req$body (JSON payload)
  if (!is.null(req$body) && is.list(req$body) && !is.null(req$body$session_id)) {
    val <- req$body$session_id
    if (length(val) > 0 && is.character(val) && nchar(val[1]) > 0) {
      return(val[1])
    }
  }
  # 2. From query string parameter
  if (!missing(session_id) && length(session_id) > 0) {
    val <- as.character(session_id)
    if (nchar(val[1]) > 0) {
      return(val[1])
    }
  }
  # 3. From header
  if (!is.null(req$HTTP_X_SESSION_ID) && nchar(req$HTTP_X_SESSION_ID) > 0) {
    return(as.character(req$HTTP_X_SESSION_ID))
  }
  return("")
}

#* @apiTitle Clickstream Analytics & ML Engine
#* @apiDescription R backend powering all calculations, aggregations, models and visualizations
#* @apiVersion 1.0.0

#* Enable CORS filter
#* @filter cors
function(req, res) {
  res$setHeader("Access-Control-Allow-Origin", "*")
  res$setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
  res$setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Session-Id")
  if (req$REQUEST_METHOD == "OPTIONS") {
    res$status <- 200
    return(list())
  }
  plumber::forward()
}

#* Health check
#* @get /health
#* @serializer unboxedJSON
function() {
  list(
    status = "ok",
    r_version = R.version.string,
    timestamp = as.character(Sys.time())
  )
}

#* Inspect dataset schema, preview, and mapping
#* @post /dataset/inspect
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    inspect_dataset(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Save field mapping
#* @post /dataset/field-mapping
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    save_field_mapping(sid, body$mapping)
    list(status = "success", message = "Field mapping saved")
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Run data preprocessing
#* @post /preprocessing/run
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    opts <- if (!is.null(body$options)) body$options else list()
    run_preprocessing(sid, opts)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Overview KPIs
#* @get /overview/kpis
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_overview_kpis(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* EDA Summary
#* @get /eda/summary
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_eda_summary(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Clickstream Analysis
#* @get /clickstream/analysis
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_clickstream_analysis(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Purchase Patterns
#* @get /purchase/patterns
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_purchase_patterns(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Conversion Funnel Analysis
#* @post /funnel/analysis
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    stages <- if (!is.null(body$stages)) body$stages else NULL
    get_funnel_analysis(sid, stages)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Customer Segmentation (RFM + k-means)
#* @get /segmentation/run
#* @serializer unboxedJSON
function(req, res, session_id = "", k = 4) {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_customer_segmentation(sid, k = as.integer(k))
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Train Conversion Prediction Models
#* @post /conversion/train
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    inc_early <- if (!is.null(body$include_early_checkout)) as.logical(body$include_early_checkout) else FALSE
    inc_cust <- if (!is.null(body$include_customer_attr)) as.logical(body$include_customer_attr) else TRUE
    train_conversion_models(sid, include_early_checkout = inc_early, include_customer_attr = inc_cust)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Train Revenue Estimation Models
#* @post /revenue/train
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    inc_cart <- if (!is.null(body$include_first_cart_item)) as.logical(body$include_first_cart_item) else TRUE
    inc_cust <- if (!is.null(body$include_customer_attr)) as.logical(body$include_customer_attr) else TRUE
    train_revenue_models(sid, include_first_cart_item = inc_cart, include_customer_attr = inc_cust)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Time-Series Analysis & Forecast
#* @get /timeseries/analysis
#* @serializer unboxedJSON
function(req, res, session_id = "", metric = "revenue", interval = "daily", forecast_periods = 14) {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_time_series_data(sid, metric = metric, interval = interval, forecast_periods = as.integer(forecast_periods))
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Visual Analytics Studio Dynamic Query
#* @post /studio/query
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    config <- if (!is.null(body$config)) body$config else body
    query_visual_studio(sid, config)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Save Visual Studio Config
#* @post /studio/save-config
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    body <- req$body
    save_studio_config(sid, body$config)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}

#* Get Visual Studio Configs
#* @get /studio/configs
#* @serializer unboxedJSON
function(req, res, session_id = "") {
  sid <- extract_sid(req, session_id)
  tryCatch({
    get_studio_configs(sid)
  }, error = function(e) {
    res$status <- 400
    list(status = "error", message = e$message)
  })
}
