# revenue_estimation.R: Order value regression, expected revenue estimation, and 30-day forecast
suppressPackageStartupMessages({
  library(data.table)
  library(randomForest)
  library(xgboost)
  library(forecast)
})
source("utils.R")

train_revenue_models <- function(session_id, include_first_cart_item = TRUE, include_customer_attr = TRUE) {
  dt <- load_session_data(session_id)
  s_path <- get_session_path(session_id)
  
  # Ensure required columns
  check_required_columns(dt, c("session_id", "event_type"))
  
  time_col <- if ("event_timestamp" %in% names(dt)) "event_timestamp" else "session_page_number"
  data.table::setorderv(dt, c("session_id", time_col))
  
  # Part A: Target = session purchase_amount (sum of purchase rows for converted sessions)
  # Find converted sessions and their total purchase amount
  purch_sessions <- dt[event_type == "purchase" | is_conversion_event == 1, .(
    session_purchase = sum(purchase_amount, na.rm = TRUE)
  ), by = session_id]
  purch_sessions <- purch_sessions[session_purchase > 0]
  
  if (nrow(purch_sessions) < 40) {
    # If purchase event not explicit, check session_converted and cart_value or max purchase_amount
    purch_sessions <- dt[session_converted == 1 & purchase_amount > 0, .(
      session_purchase = max(purchase_amount, na.rm = TRUE)
    ), by = session_id]
  }
  
  if (nrow(purch_sessions) < 30) {
    stop("Insufficient converted sessions with positive purchase amount for regression training.")
  }
  
  # Find first add_to_cart event for each converted session
  first_carts <- dt[event_type == "add_to_cart", .(
    first_cart_page = min(session_page_number, na.rm = TRUE),
    cart_prod_price = if ("product_price" %in% names(dt)) head(product_price, 1) else 0,
    cart_prod_category = if ("product_category" %in% names(dt)) head(product_category, 1) else "General"
  ), by = session_id]
  
  # Merge converted sessions with their first cart info
  reg_cohort <- merge(purch_sessions, first_carts, by = "session_id", all.x = TRUE)
  reg_cohort[is.na(first_cart_page), first_cart_page := 999]
  reg_cohort[is.na(cart_prod_price), cart_prod_price := 0]
  reg_cohort[is.na(cart_prod_category), cart_prod_category := "General"]
  
  # Pre-cart events
  dt_pre <- merge(dt[session_id %in% reg_cohort$session_id], reg_cohort[, .(session_id, first_cart_page)], by = "session_id")
  dt_pre <- dt_pre[session_page_number < first_cart_page]
  
  has_timestamp <- "event_timestamp" %in% names(dt)
  
  # Allowlisted browsing features
  feats <- dt_pre[, .(
    count_home = sum(event_type == "home", na.rm = TRUE),
    count_search = sum(event_type == "search", na.rm = TRUE),
    count_cat_view = sum(event_type == "category_view", na.rm = TRUE),
    count_prod_view = sum(event_type == "product_view", na.rm = TRUE),
    count_wishlist = sum(event_type == "wishlist", na.rm = TRUE),
    distinct_prods_viewed = if ("product_id" %in% names(dt_pre)) data.table::uniqueN(na.omit(product_id[product_id != ""])) else 0,
    distinct_cats_viewed = if ("product_category" %in% names(dt_pre)) data.table::uniqueN(na.omit(product_category[product_category != ""])) else 0,
    total_time_on_page = if ("time_on_page_seconds" %in% names(dt_pre)) sum(time_on_page_seconds, na.rm = TRUE) else 0,
    avg_time_on_page = if ("time_on_page_seconds" %in% names(dt_pre)) mean(time_on_page_seconds, na.rm = TRUE) else 0,
    device_type = if ("device_type" %in% names(dt_pre)) head(device_type, 1) else "Desktop",
    traffic_source = if ("traffic_source" %in% names(dt_pre)) head(traffic_source, 1) else "Direct",
    session_start_time = if (has_timestamp) min(event_timestamp, na.rm = TRUE) else as.POSIXct(Sys.time()),
    session_hour = if ("session_hour" %in% names(dt_pre)) head(session_hour, 1) 
                   else if (has_timestamp) as.integer(format(min(event_timestamp, na.rm = TRUE), "%H")) else 12,
    is_weekend = if ("is_weekend" %in% names(dt_pre)) head(is_weekend, 1) else 0,
    # Customer attributes
    clv = if (include_customer_attr && "customer_lifetime_value" %in% names(dt_pre)) head(customer_lifetime_value, 1) else 0,
    hist_aov = if (include_customer_attr && "historical_average_order_value" %in% names(dt_pre)) head(historical_average_order_value, 1) else 0,
    prev_purch = if (include_customer_attr && "previous_purchase_count" %in% names(dt_pre)) head(previous_purchase_count, 1) else 0,
    cust_segment = if (include_customer_attr && "customer_segment" %in% names(dt_pre)) head(customer_segment, 1) else "Standard"
  ), by = session_id]
  
  df_reg <- merge(feats, reg_cohort[, .(session_id, session_purchase, cart_prod_price, cart_prod_category)], by = "session_id")
  
  # Fill NAs
  for (cn in names(df_reg)) {
    if (is.numeric(df_reg[[cn]])) {
      df_reg[is.na(get(cn)), (cn) := 0]
    }
  }
  
  # Chronological sort
  data.table::setorder(df_reg, session_start_time)
  
  # 80/20 Chronological train/test split
  n_rows <- nrow(df_reg)
  split_idx <- floor(0.8 * n_rows)
  train_reg <- df_reg[1:split_idx]
  test_reg <- df_reg[(split_idx + 1):n_rows]
  
  # Features list
  feature_cols <- c(
    "count_home", "count_search", "count_cat_view", "count_prod_view", "count_wishlist",
    "distinct_prods_viewed", "distinct_cats_viewed", "total_time_on_page", "avg_time_on_page",
    "session_hour", "is_weekend"
  )
  if (include_customer_attr) {
    feature_cols <- c(feature_cols, "clv", "hist_aov", "prev_purch")
  }
  if (include_first_cart_item) {
    feature_cols <- c(feature_cols, "cart_prod_price")
  }
  
  y_test <- test_reg$session_purchase
  mean_baseline_pred <- rep(mean(train_reg$session_purchase), length(y_test))
  baseline_rmse <- round(sqrt(mean((y_test - mean_baseline_pred)^2)), 2)
  baseline_mae <- round(mean(abs(y_test - mean_baseline_pred)), 2)
  
  calc_reg_metrics <- function(y_true, y_pred) {
    rmse <- round(sqrt(mean((y_true - y_pred)^2)), 2)
    mae <- round(mean(abs(y_true - y_pred)), 2)
    rss <- sum((y_true - y_pred)^2)
    tss <- sum((y_true - mean(y_true))^2)
    r2 <- round(max(0, 1 - (rss / pmax(1e-5, tss))), 4)
    list(rmse = rmse, mae = mae, r_squared = r2)
  }
  
  # 1. Linear Model (lm)
  fmla <- as.formula(paste("session_purchase ~", paste(feature_cols, collapse = " + ")))
  lm_fit <- lm(fmla, data = train_reg)
  lm_pred <- pmax(0, predict(lm_fit, newdata = test_reg))
  lm_pred[is.na(lm_pred)] <- mean(train_reg$session_purchase)
  lm_metrics <- calc_reg_metrics(y_test, lm_pred)
  
  # 2. Random Forest Regressor
  rf_fit <- randomForest::randomForest(fmla, data = train_reg, ntree = 100, mtry = 3)
  rf_pred <- pmax(0, predict(rf_fit, newdata = test_reg))
  rf_metrics <- calc_reg_metrics(y_test, rf_pred)
  
  # 3. XGBoost Regressor
  x_train_mat <- model.matrix(fmla, data = train_reg)[, -1]
  x_test_mat <- model.matrix(fmla, data = test_reg)[, -1]
  
  dtrain_reg <- xgboost::xgb.DMatrix(data = x_train_mat, label = train_reg$session_purchase)
  dtest_reg <- xgboost::xgb.DMatrix(data = x_test_mat, label = test_reg$session_purchase)
  
  xgb_reg <- xgboost::xgb.train(
    params = list(objective = "reg:squarederror", max_depth = 4, eta = 0.1),
    data = dtrain_reg, nrounds = 50, verbose = 0
  )
  xgb_pred <- pmax(0, predict(xgb_reg, dtest_reg))
  xgb_metrics <- calc_reg_metrics(y_test, xgb_pred)
  
  # Best model by RMSE
  rmses <- c("Linear Regression" = lm_metrics$rmse, "Random Forest" = rf_metrics$rmse, "XGBoost" = xgb_metrics$rmse)
  best_reg_name <- names(which.min(rmses))
  best_reg_pred <- switch(best_reg_name,
    "Linear Regression" = lm_pred,
    "Random Forest" = rf_pred,
    "XGBoost" = xgb_pred
  )
  
  # Residuals and predicted vs actual scatter data (sample 100 points for chart)
  chart_sample_idx <- sample(length(y_test), min(100, length(y_test)))
  pred_vs_actual <- lapply(chart_sample_idx, function(i) {
    list(
      actual = round(y_test[i], 2),
      predicted = round(best_reg_pred[i], 2),
      residual = round(y_test[i] - best_reg_pred[i], 2)
    )
  })
  
  # RF Feature importance
  rf_imp <- randomForest::importance(rf_fit)
  imp_df <- data.frame(feature = rownames(rf_imp), importance = round(unname(rf_imp[, 1]), 2))
  imp_df <- imp_df[order(-imp_df$importance), ]
  feat_importance <- lapply(1:min(10, nrow(imp_df)), function(i) {
    list(feature = as.character(imp_df$feature[i]), importance = as.numeric(imp_df$importance[i]))
  })
  
  # Part B: Expected Revenue per Session = P(convert) from Classifier * Predicted Order Value
  # Load classification model if available, else estimate conversion probability
  conv_rds_path <- file.path(s_path, "conversion_models.rds")
  p_convert <- rep(0.15, nrow(test_reg))
  if (file.exists(conv_rds_path)) {
    conv_art <- readRDS(conv_rds_path)
    # Check if matching sessions exist
    matched_idx <- match(test_reg$session_id, conv_art$test_df$session_id)
    valid_matches <- !is.na(matched_idx)
    if (any(valid_matches)) {
      p_convert[valid_matches] <- conv_art$best_probs[matched_idx[valid_matches]]
    }
  }
  
  expected_rev_per_session <- p_convert * best_reg_pred
  total_expected_revenue <- round(sum(expected_rev_per_session), 2)
  total_actual_revenue <- round(sum(y_test), 2)
  
  # Breakdown by Device, Traffic, Customer Segment
  expected_by_device <- test_reg[, .(
    sessions = .N,
    actual_rev = sum(session_purchase, na.rm = TRUE),
    expected_rev = sum(expected_rev_per_session[.I], na.rm = TRUE)
  ), by = device_type]
  
  expected_device_list <- lapply(1:nrow(expected_by_device), function(i) {
    list(
      device = as.character(expected_by_device$device_type[i]),
      actual = round(as.numeric(expected_by_device$actual_rev[i]), 2),
      expected = round(as.numeric(expected_by_device$expected_rev[i]), 2)
    )
  })
  
  expected_by_traffic <- test_reg[, .(
    sessions = .N,
    actual_rev = sum(session_purchase, na.rm = TRUE),
    expected_rev = sum(expected_rev_per_session[.I], na.rm = TRUE)
  ), by = traffic_source]
  
  expected_traffic_list <- lapply(1:nrow(expected_by_traffic), function(i) {
    list(
      traffic = as.character(expected_by_traffic$traffic_source[i]),
      actual = round(as.numeric(expected_by_traffic$actual_rev[i]), 2),
      expected = round(as.numeric(expected_by_traffic$expected_rev[i]), 2)
    )
  })
  
  # Part C: Revenue Forecast with forecast package (next 30 days) from daily revenue
  daily_rev <- dt[!is.na(event_timestamp) & (event_type == "purchase" | is_conversion_event == 1), .(
    rev = sum(purchase_amount, na.rm = TRUE)
  ), by = .(date = as.Date(event_timestamp))][order(date)]
  
  forecast_30d <- list()
  if (nrow(daily_rev) >= 7) {
    rev_ts <- ts(daily_rev$rev, frequency = 7)
    fc_fit <- tryCatch(forecast::auto.arima(rev_ts), error = function(e) forecast::ets(rev_ts))
    fc_obj <- forecast::forecast(fc_fit, h = 30)
    last_d <- max(daily_rev$date)
    f_dates <- as.character(last_d + 1:30)
    forecast_30d <- lapply(1:30, function(i) {
      list(
        date = f_dates[i],
        forecast = round(max(0, as.numeric(fc_obj$mean[i])), 2),
        lower_80 = round(max(0, as.numeric(fc_obj$lower[i, 1])), 2),
        upper_80 = round(max(0, as.numeric(fc_obj$upper[i, 1])), 2),
        lower_95 = round(max(0, as.numeric(fc_obj$lower[i, 2])), 2),
        upper_95 = round(max(0, as.numeric(fc_obj$upper[i, 2])), 2)
      )
    })
  }
  
  # Save revenue predictions CSV for download
  rev_csv_df <- data.frame(
    session_id = test_reg$session_id,
    actual_order_value = round(y_test, 2),
    predicted_order_value = round(best_reg_pred, 2),
    predicted_p_convert = round(p_convert, 4),
    expected_revenue = round(expected_rev_per_session, 2),
    device_type = test_reg$device_type,
    traffic_source = test_reg$traffic_source
  )
  data.table::fwrite(rev_csv_df, file.path(s_path, "revenue_predictions.csv"))
  
  return(list(
    part_a = list(
      train_sessions = nrow(train_reg),
      test_sessions = nrow(test_reg),
      mean_baseline = list(rmse = baseline_rmse, mae = baseline_mae),
      models = list(
        list(name = "Linear Regression", metrics = lm_metrics),
        list(name = "Random Forest", metrics = rf_metrics),
        list(name = "XGBoost", metrics = xgb_metrics)
      ),
      best_model = best_reg_name,
      predicted_vs_actual = pred_vs_actual,
      feature_importance = feat_importance
    ),
    part_b = list(
      total_expected_revenue = total_expected_revenue,
      total_actual_revenue = total_actual_revenue,
      by_device = expected_device_list,
      by_traffic = expected_traffic_list
    ),
    part_c = list(
      forecast_days = 30,
      daily_forecast = forecast_30d
    )
  ))
}
