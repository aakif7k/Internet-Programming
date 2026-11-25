# utils.R: Helper functions for dataset handling, session resolution, and field mapping

# Ensure local r-library is in .libPaths
base_dir <- normalizePath(file.path(getwd(), ".."), winslash = "/", mustWork = FALSE)
lib_dir <- file.path(base_dir, "r-library")
if (!dir.exists(lib_dir)) {
  lib_dir <- normalizePath(file.path(getwd(), "r-library"), winslash = "/", mustWork = FALSE)
}
if (dir.exists(lib_dir)) {
  .libPaths(c(lib_dir, .libPaths()))
}

suppressPackageStartupMessages({
  library(data.table)
  library(dplyr)
  library(tidyr)
  library(jsonlite)
})

SESSION_DIR_BASE <- Sys.getenv("SESSION_DIR", unset = file.path(dirname(getwd()), "temp_sessions"))
if (!dir.exists(SESSION_DIR_BASE)) {
  if (dir.exists("temp_sessions")) {
    SESSION_DIR_BASE <- normalizePath("temp_sessions")
  } else if (dir.exists("../temp_sessions")) {
    SESSION_DIR_BASE <- normalizePath("../temp_sessions")
  } else {
    dir.create(SESSION_DIR_BASE, recursive = TRUE, showWarnings = FALSE)
  }
}

get_session_path <- function(session_id) {
  if (is.null(session_id) || length(session_id) == 0 || is.na(session_id[1]) || nchar(session_id[1]) == 0) {
    stop("No dataset uploaded for this session. Please upload a dataset first.")
  }
  sid <- as.character(session_id[1])
  safe_id <- gsub("[^a-zA-Z0-9_-]", "", sid)
  if (nchar(safe_id) == 0) {
    stop("No dataset uploaded for this session. Please upload a dataset first.")
  }
  s_path <- file.path(SESSION_DIR_BASE, safe_id)
  if (!dir.exists(s_path)) {
    dir.create(s_path, recursive = TRUE, showWarnings = FALSE)
  }
  return(s_path)
}

get_field_mapping <- function(session_id) {
  s_path <- get_session_path(session_id)
  map_file <- file.path(s_path, "field_mapping.json")
  if (file.exists(map_file)) {
    tryCatch({
      return(jsonlite::fromJSON(map_file))
    }, error = function(e) list())
  }
  return(list())
}

save_field_mapping <- function(session_id, mapping) {
  s_path <- get_session_path(session_id)
  map_file <- file.path(s_path, "field_mapping.json")
  jsonlite::write_json(mapping, map_file, auto_unbox = TRUE, pretty = TRUE)
}

get_active_dataset_path <- function(session_id) {
  s_path <- get_session_path(session_id)
  cleaned <- file.path(s_path, "cleaned_clickstream.csv")
  raw <- file.path(s_path, "raw_clickstream.csv")
  
  if (file.exists(cleaned[1])) {
    return(list(path = cleaned[1], type = "cleaned"))
  } else if (file.exists(raw[1])) {
    return(list(path = raw[1], type = "raw"))
  } else {
    return(NULL)
  }
}

load_session_data <- function(session_id, apply_mapping = TRUE) {
  ds_info <- get_active_dataset_path(session_id)
  if (is.null(ds_info)) {
    stop("No dataset uploaded for this session. Please upload a dataset first.")
  }
  
  # Read fast using data.table
  dt <- data.table::fread(ds_info$path, stringsAsFactors = FALSE, na.strings = c("NA", "", "null", "None", "NULL"))
  
  # Apply user field mapping if present
  if (apply_mapping) {
    mapping <- get_field_mapping(session_id)
    if (length(mapping) > 0) {
      for (std_col in names(mapping)) {
        user_col <- mapping[[std_col]]
        if (!is.null(user_col) && user_col != "" && user_col %in% names(dt) && user_col != std_col) {
          data.table::setnames(dt, old = user_col, new = std_col)
        }
      }
    }
  }
  
  # Standard auto-conversions for common expected columns
  if ("event_timestamp" %in% names(dt)) {
    parsed_vals <- as.POSIXct(as.character(dt$event_timestamp), format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
    if (all(is.na(parsed_vals)) && nrow(dt) > 0) {
      parsed_vals <- tryCatch(as.POSIXct(as.character(dt$event_timestamp), tz = "UTC"), error = function(e) rep(as.POSIXct(NA), nrow(dt)))
    }
    dt[, event_timestamp := parsed_vals]
  }
  
  # Numeric conversions for key metrics
  numeric_cols <- c("product_price", "quantity", "cart_value", "purchase_amount", 
                    "session_page_number", "time_on_page_seconds", "customer_lifetime_value",
                    "previous_purchase_count", "historical_average_order_value", "customer_tenure_days",
                    "discount_percent", "session_converted", "is_conversion_event")
  for (nc in numeric_cols) {
    if (nc %in% names(dt)) {
      dt[[nc]] <- suppressWarnings(as.numeric(dt[[nc]]))
    }
  }
  
  return(dt)
}

check_required_columns <- function(dt, required_cols) {
  missing_cols <- setdiff(required_cols, names(dt))
  if (length(missing_cols) > 0) {
    stop(paste("Missing required column(s):", paste(missing_cols, collapse = ", "), 
               ". Please check the Field Mapping in Dataset Upload."))
  }
  invisible(TRUE)
}

safe_json_response <- function(data) {
  jsonlite::toJSON(data, auto_unbox = TRUE, digits = 4, na = "null", null = "null", force = TRUE)
}
