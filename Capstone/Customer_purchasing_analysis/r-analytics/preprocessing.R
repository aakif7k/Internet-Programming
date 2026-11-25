# preprocessing.R: Dataset inspection, field mapping auto-detection, and data cleansing
source("utils.R")

standard_fields <- c(
  "event_id", "customer_id", "session_id", "event_timestamp", "event_type",
  "page_url", "product_id", "product_name", "product_category", "product_price",
  "quantity", "device_type", "traffic_source", "visitor_type", "browser", "country",
  "session_page_number", "time_on_page_seconds", "cart_value", "purchase_amount",
  "is_conversion_event", "session_converted", "customer_segment",
  "customer_lifetime_value", "previous_purchase_count", "historical_average_order_value",
  "customer_tenure_days", "loyalty_member", "discount_percent"
)

inspect_dataset <- function(session_id) {
  ds_info <- get_active_dataset_path(session_id)
  if (is.null(ds_info)) {
    return(list(status = "empty", message = "No dataset uploaded"))
  }
  
  # Read preview (first 50 rows) and column metadata
  dt_sample <- data.table::fread(ds_info$path, nrows = 50, stringsAsFactors = FALSE)
  
  # Read total line count reliably and fast
  dt_count <- data.table::fread(ds_info$path, select = 1L)
  total_rows <- nrow(dt_count)
  
  all_cols <- names(dt_sample)
  
  # Missing counts and data types on sample or full
  # To be fast and accurate on 96k rows:
  dt_header_types <- sapply(dt_sample, function(x) {
    if (is.numeric(x)) return("numeric")
    if (is.integer(x)) return("integer")
    if (is.logical(x)) return("boolean")
    return("character")
  })
  
  # Check duplicates and missing on sample
  dt_est <- data.table::fread(ds_info$path, nrows = 25000, stringsAsFactors = FALSE)
  missing_counts <- sapply(dt_est, function(x) {
    if (is.character(x)) {
      sum(is.na(x) | x == "" | x == "NA" | x == "null")
    } else {
      sum(is.na(x))
    }
  })
  missing_pcts <- round((missing_counts / nrow(dt_est)) * 100, 1)
  
  duplicates_sample <- sum(duplicated(dt_est))
  
  # Field mapping suggestions
  mapping_suggestions <- list()
  lower_cols <- tolower(all_cols)
  for (std in standard_fields) {
    std_low <- tolower(std)
    # Exact match
    if (std %in% all_cols) {
      mapping_suggestions[[std]] <- std
    } else {
      # Fuzzy or partial match
      idx <- which(lower_cols == std_low)
      if (length(idx) > 0) {
        mapping_suggestions[[std]] <- all_cols[idx[1]]
      } else {
        # Check synonyms
        synonyms <- list(
          event_timestamp = c("timestamp", "datetime", "time", "date"),
          event_type = c("action", "event", "type"),
          session_id = c("sess_id", "session"),
          customer_id = c("user_id", "cust_id", "client_id"),
          purchase_amount = c("revenue", "amount", "order_value", "total_price")
        )
        if (std %in% names(synonyms)) {
          syn_match <- intersect(lower_cols, synonyms[[std]])
          if (length(syn_match) > 0) {
            mapping_suggestions[[std]] <- all_cols[which(lower_cols == syn_match[1])[1]]
          }
        }
      }
    }
  }
  
  # Format preview table for frontend
  preview_rows <- lapply(1:nrow(dt_sample), function(i) as.list(dt_sample[i, ]))
  
  column_meta <- lapply(all_cols, function(col) {
    list(
      name = col,
      type = unname(dt_header_types[col]),
      missing_count = as.integer(missing_counts[col]),
      missing_pct = as.numeric(missing_pcts[col]),
      sample_values = as.character(na.omit(dt_sample[[col]]))[1:3]
    )
  })
  
  saved_mapping <- get_field_mapping(session_id)
  
  return(list(
    status = "ready",
    active_type = ds_info$type,
    filename = basename(ds_info$path),
    total_rows = total_rows,
    total_columns = length(all_cols),
    columns = column_meta,
    preview = preview_rows,
    duplicate_count_est = duplicates_sample,
    standard_fields = standard_fields,
    auto_mapping = mapping_suggestions,
    saved_mapping = saved_mapping
  ))
}

run_preprocessing <- function(session_id, options = list()) {
  s_path <- get_session_path(session_id)
  raw_file <- file.path(s_path, "raw_clickstream.csv")
  cleaned_file <- file.path(s_path, "cleaned_clickstream.csv")
  
  if (!file.exists(raw_file)) {
    stop("Raw dataset not found. Please upload a dataset first.")
  }
  
  count_table_missing <- function(d) {
    sum(sapply(d, function(col) {
      if (is.character(col)) sum(is.na(col) | col == "" | col == "NA" | col == "null")
      else sum(is.na(col))
    }))
  }

  # Load raw data
  dt <- data.table::fread(raw_file, stringsAsFactors = FALSE)
  initial_rows <- nrow(dt)
  initial_missing <- count_table_missing(dt)
  
  # Default options
  remove_duplicates <- ifelse(is.null(options$remove_duplicates), TRUE, as.logical(options$remove_duplicates))
  handle_missing <- ifelse(is.null(options$handle_missing), "impute", as.character(options$handle_missing)) # "drop", "impute", "keep"
  parse_dates <- ifelse(is.null(options$parse_dates), TRUE, as.logical(options$parse_dates))
  filter_outliers <- ifelse(is.null(options$filter_outliers), FALSE, as.logical(options$filter_outliers))
  
  # 1. Duplicates
  duplicates_removed <- 0
  if (remove_duplicates) {
    dup_idx <- duplicated(dt)
    duplicates_removed <- sum(dup_idx)
    if (duplicates_removed > 0) {
      dt <- dt[!dup_idx]
    }
  }
  
  # 2. Timestamp parsing
  invalid_dates_dropped <- 0
  if (parse_dates && "event_timestamp" %in% names(dt)) {
    parsed_vals <- as.POSIXct(as.character(dt$event_timestamp), format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
    if (all(is.na(parsed_vals)) && nrow(dt) > 0) {
      parsed_vals <- tryCatch(as.POSIXct(as.character(dt$event_timestamp), tz = "UTC"), error = function(e) rep(as.POSIXct(NA), nrow(dt)))
    }
    dt[, parsed_time := parsed_vals]
    invalid_dates_dropped <- sum(is.na(dt$parsed_time))
    if (invalid_dates_dropped > 0 && handle_missing == "drop") {
      dt <- dt[!is.na(parsed_time)]
    }
    # Keep standard POSIXct timestamp
    dt[!is.na(parsed_time), event_timestamp := parsed_time]
    dt[, parsed_time := NULL]
  }
  
  # 3. Missing values handling
  rows_dropped_missing <- 0
  imputed_count <- 0
  
  if (handle_missing == "drop") {
    # Drop rows with NA in crucial identifiers
    key_cols <- intersect(c("event_id", "session_id", "customer_id", "event_type"), names(dt))
    if (length(key_cols) > 0) {
      complete_keys <- complete.cases(dt[, ..key_cols])
      rows_dropped_missing <- sum(!complete_keys)
      dt <- dt[complete_keys]
    }
  } else if (handle_missing == "impute") {
    # Impute numeric columns with median, categorical with "Unknown" or mode
    for (col in names(dt)) {
      if (is.numeric(dt[[col]])) {
        na_mask <- is.na(dt[[col]])
        if (any(na_mask)) {
          med_val <- median(dt[[col]], na.rm = TRUE)
          if (is.na(med_val)) med_val <- 0
          data.table::set(dt, which(na_mask), col, med_val)
          imputed_count <- imputed_count + sum(na_mask)
        }
      } else if (is.character(dt[[col]])) {
        na_mask <- is.na(dt[[col]]) | dt[[col]] == "" | dt[[col]] == "NA"
        if (any(na_mask)) {
          data.table::set(dt, which(na_mask), col, "Unknown")
          imputed_count <- imputed_count + sum(na_mask)
        }
      }
    }
  }
  
  # 4. Outlier handling (IQR clipping or removal for key monetary/time columns)
  outliers_handled <- 0
  if (filter_outliers) {
    num_cols_to_check <- intersect(c("purchase_amount", "cart_value", "time_on_page_seconds"), names(dt))
    for (cname in num_cols_to_check) {
      vals <- dt[[cname]]
      pos_vals <- vals[vals > 0 & !is.na(vals)]
      if (length(pos_vals) > 100) {
        q25 <- quantile(pos_vals, 0.25, na.rm = TRUE)
        q75 <- quantile(pos_vals, 0.75, na.rm = TRUE)
        iqr <- q75 - q25
        upper_limit <- q75 + 3 * iqr # conservative 3x IQR
        out_mask <- vals > upper_limit
        outliers_handled <- outliers_handled + sum(out_mask, na.rm = TRUE)
        # Cap at upper_limit rather than deleting row
        data.table::set(dt, which(out_mask), cname, upper_limit)
      }
    }
  }
  
  # Write cleaned CSV (NEVER modify raw_clickstream.csv!)
  data.table::fwrite(dt, cleaned_file)
  
  final_rows <- nrow(dt)
  final_missing <- count_table_missing(dt)
  
  return(list(
    status = "success",
    message = "Preprocessing completed and cleaned dataset saved.",
    summary = list(
      initial_rows = initial_rows,
      final_rows = final_rows,
      rows_removed = initial_rows - final_rows,
      duplicates_removed = duplicates_removed,
      initial_missing = initial_missing,
      final_missing = final_missing,
      imputed_values = imputed_count,
      outliers_handled = outliers_handled
    )
  ))
}
