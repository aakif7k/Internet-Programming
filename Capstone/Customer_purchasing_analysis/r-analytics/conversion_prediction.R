# conversion_prediction.R: Session-level conversion modeling following strict allowlist and chronological split
suppressPackageStartupMessages({
  library(data.table)
  library(rpart)
  library(randomForest)
  library(xgboost)
  library(pROC)
})
source("utils.R")

prepare_conversion_cohort <- function(dt, include_early_checkout = FALSE, include_customer_attr = TRUE) {
  # Sort chronologically
  time_col <- if ("event_timestamp" %in% names(dt)) "event_timestamp" else "session_page_number"
  data.table::setorderv(dt, c("session_id", time_col))
  
  # Find first add_to_cart event per session
  cart_events <- dt[event_type == "add_to_cart", .(
    first_cart_page = min(session_page_number, na.rm = TRUE),
    first_cart_time = if ("event_timestamp" %in% names(dt)) min(event_timestamp, na.rm = TRUE) else NA
  ), by = session_id]
  
  if (nrow(cart_events) == 0) {
    stop("No add_to_cart events found in the dataset. Cannot construct add_to_cart prediction cohort.")
  }
  
  # Check for early checkouts before first add_to_cart
  checkouts <- dt[event_type == "checkout", .(
    first_checkout_page = min(session_page_number, na.rm = TRUE)
  ), by = session_id]
  
  cohort_meta <- merge(cart_events, checkouts, by = "session_id", all.x = TRUE)
  
  # Cohort filter
  if (!include_early_checkout) {
    valid_sessions <- cohort_meta[is.na(first_checkout_page) | first_checkout_page >= first_cart_page, session_id]
  } else {
    valid_sessions <- cohort_meta$session_id
  }
  
  # Target = session_converted (0 or 1)
  # Pre-calculate session target
  if ("session_converted" %in% names(dt)) {
    target_dt <- dt[session_id %in% valid_sessions, .(
      target = as.integer(max(session_converted, na.rm = TRUE) == 1)
    ), by = session_id]
  } else {
    target_dt <- dt[session_id %in% valid_sessions, .(
      target = as.integer(any(event_type == "purchase" | event_type == "checkout"))
    ), by = session_id]
  }
  
  # Filter events strictly BEFORE first add_to_cart (cut by session_page_number)
  dt_cohort <- merge(dt[session_id %in% valid_sessions], cohort_meta[, .(session_id, first_cart_page)], by = "session_id")
  dt_pre_cart <- dt_cohort[session_page_number < first_cart_page]
  
  # Engineer features STRICTLY from allowlist:
  # - counts of home, search, category_view, product_view, wishlist
  # - distinct products and categories viewed
  # - total and average time on page
  # - session start time, device, traffic, browser, country, hour, day_of_week, is_weekend
  
  has_timestamp <- "event_timestamp" %in% names(dt)
  
  feats <- dt_pre_cart[, .(
    count_home = sum(event_type == "home", na.rm = TRUE),
    count_search = sum(event_type == "search", na.rm = TRUE),
    count_cat_view = sum(event_type == "category_view", na.rm = TRUE),
    count_prod_view = sum(event_type == "product_view", na.rm = TRUE),
    count_wishlist = sum(event_type == "wishlist", na.rm = TRUE),
    distinct_prods_viewed = if ("product_id" %in% names(dt_pre_cart)) data.table::uniqueN(na.omit(product_id[product_id != ""])) else 0,
    distinct_cats_viewed = if ("product_category" %in% names(dt_pre_cart)) data.table::uniqueN(na.omit(product_category[product_category != ""])) else 0,
    total_time_on_page = if ("time_on_page_seconds" %in% names(dt_pre_cart)) sum(time_on_page_seconds, na.rm = TRUE) else 0,
    avg_time_on_page = if ("time_on_page_seconds" %in% names(dt_pre_cart)) mean(time_on_page_seconds, na.rm = TRUE) else 0,
    device_type = if ("device_type" %in% names(dt_pre_cart)) head(device_type, 1) else "Desktop",
    traffic_source = if ("traffic_source" %in% names(dt_pre_cart)) head(traffic_source, 1) else "Direct",
    browser = if ("browser" %in% names(dt_pre_cart)) head(browser, 1) else "Chrome",
    country = if ("country" %in% names(dt_pre_cart)) head(country, 1) else "Unknown",
    session_start_time = if (has_timestamp) min(event_timestamp, na.rm = TRUE) else as.POSIXct(Sys.time()),
    session_hour = if ("session_hour" %in% names(dt_pre_cart)) head(session_hour, 1) 
                   else if (has_timestamp) as.integer(format(min(event_timestamp, na.rm = TRUE), "%H")) else 12,
    day_of_week = if ("day_of_week" %in% names(dt_pre_cart)) head(day_of_week, 1)
                  else if (has_timestamp) format(min(event_timestamp, na.rm = TRUE), "%A") else "Monday",
    is_weekend = if ("is_weekend" %in% names(dt_pre_cart)) head(is_weekend, 1) else 0,
    # Customer attributes
    clv = if (include_customer_attr && "customer_lifetime_value" %in% names(dt_pre_cart)) head(customer_lifetime_value, 1) else 0,
    hist_aov = if (include_customer_attr && "historical_average_order_value" %in% names(dt_pre_cart)) head(historical_average_order_value, 1) else 0,
    prev_purch = if (include_customer_attr && "previous_purchase_count" %in% names(dt_pre_cart)) head(previous_purchase_count, 1) else 0,
    cust_segment = if (include_customer_attr && "customer_segment" %in% names(dt_pre_cart)) head(customer_segment, 1) else "Standard",
    loyalty_member = if (include_customer_attr && "loyalty_member" %in% names(dt_pre_cart)) head(loyalty_member, 1) else 0,
    cust_tenure = if (include_customer_attr && "customer_tenure_days" %in% names(dt_pre_cart)) head(customer_tenure_days, 1) else 0
  ), by = session_id]
  
  # Merge with target
  model_df <- merge(feats, target_dt, by = "session_id")
  
  # Fill any NAs
  model_df[is.na(avg_time_on_page), avg_time_on_page := 0]
  model_df[is.na(total_time_on_page), total_time_on_page := 0]
  model_df[is.na(clv), clv := 0]
  model_df[is.na(hist_aov), hist_aov := 0]
  model_df[is.na(prev_purch), prev_purch := 0]
  model_df[is.na(cust_tenure), cust_tenure := 0]
  model_df[is.na(loyalty_member), loyalty_member := 0]
  model_df[is.na(is_weekend), is_weekend := 0]
  
  # Chronological order
  data.table::setorder(model_df, session_start_time)
  
  return(model_df)
}

train_conversion_models <- function(session_id, include_early_checkout = FALSE, include_customer_attr = TRUE) {
  dt <- load_session_data(session_id)
  s_path <- get_session_path(session_id)
  
  df <- prepare_conversion_cohort(dt, include_early_checkout = include_early_checkout, include_customer_attr = include_customer_attr)
  
  n_total <- nrow(df)
  if (n_total < 100) {
    stop("Insufficient sessions in add_to_cart cohort (less than 100).")
  }
  
  # 80/20 Chronological Split
  split_idx <- floor(0.8 * n_total)
  train_df <- df[1:split_idx]
  test_df <- df[(split_idx + 1):n_total]
  
  # Feature columns
  feature_cols <- c(
    "count_home", "count_search", "count_cat_view", "count_prod_view", "count_wishlist",
    "distinct_prods_viewed", "distinct_cats_viewed", "total_time_on_page", "avg_time_on_page",
    "session_hour", "is_weekend"
  )
  if (include_customer_attr) {
    feature_cols <- c(feature_cols, "clv", "hist_aov", "prev_purch", "loyalty_member", "cust_tenure")
  }
  
  # Factor columns
  train_df$device_type <- as.factor(train_df$device_type)
  train_df$traffic_source <- as.factor(train_df$traffic_source)
  test_df$device_type <- factor(test_df$device_type, levels = levels(train_df$device_type))
  test_df$traffic_source <- factor(test_df$traffic_source, levels = levels(train_df$traffic_source))
  
  # Majority class baseline
  y_test <- test_df$target
  majority_class <- as.integer(mean(train_df$target) >= 0.5)
  majority_baseline_acc <- round(mean(y_test == majority_class), 4)
  
  # Helper to compute classification metrics
  eval_metrics <- function(y_true, y_prob) {
    y_pred <- as.integer(y_prob >= 0.5)
    tp <- sum(y_true == 1 & y_pred == 1)
    tn <- sum(y_true == 0 & y_pred == 0)
    fp <- sum(y_true == 0 & y_pred == 1)
    fn <- sum(y_true == 1 & y_pred == 0)
    
    accuracy <- round((tp + tn) / length(y_true), 4)
    precision <- round(ifelse(tp + fp > 0, tp / (tp + fp), 0), 4)
    recall <- round(ifelse(tp + fn > 0, tp / (tp + fn), 0), 4)
    f1 <- round(ifelse(precision + recall > 0, 2 * precision * recall / (precision + recall), 0), 4)
    
    roc_obj <- pROC::roc(y_true, y_prob, quiet = TRUE)
    auc_val <- round(as.numeric(pROC::auc(roc_obj)), 4)
    
    # Coordinates for ROC Curve (sample 50 points)
    roc_coords <- data.frame(fpr = 1 - roc_obj$specificities, tpr = roc_obj$sensitivities)
    roc_coords <- roc_coords[order(roc_coords$fpr), ]
    # Sample down if large
    step_seq <- unique(round(seq(1, nrow(roc_coords), length.out = min(50, nrow(roc_coords)))))
    sampled_roc <- lapply(step_seq, function(i) {
      list(fpr = round(roc_coords$fpr[i], 3), tpr = round(roc_coords$tpr[i], 3))
    })
    
    list(
      accuracy = accuracy,
      precision = precision,
      recall = recall,
      f1 = f1,
      auc = auc_val,
      confusion_matrix = list(tp = tp, tn = tn, fp = fp, fn = fn),
      roc_curve = sampled_roc
    )
  }
  
  # 1. Logistic Regression
  fmla <- as.formula(paste("target ~", paste(c(feature_cols, "device_type", "traffic_source"), collapse = " + ")))
  lr_model <- glm(fmla, data = train_df, family = binomial(link = "logit"))
  lr_prob <- predict(lr_model, newdata = test_df, type = "response")
  lr_prob[is.na(lr_prob)] <- mean(train_df$target)
  lr_metrics <- eval_metrics(y_test, lr_prob)
  
  # 2. Decision Tree (rpart)
  dt_model <- rpart::rpart(fmla, data = train_df, method = "class", control = rpart::rpart.control(cp = 0.005, maxdepth = 6))
  dt_prob_mat <- predict(dt_model, newdata = test_df, type = "prob")
  dt_prob <- dt_prob_mat[, "1"]
  dt_metrics <- eval_metrics(y_test, dt_prob)
  
  # 3. Random Forest (randomForest)
  rf_train <- data.table::copy(train_df)
  rf_train$target <- as.factor(rf_train$target)
  rf_test <- data.table::copy(test_df)
  rf_test$target <- factor(rf_test$target, levels = levels(rf_train$target))
  
  rf_model <- randomForest::randomForest(
    fmla, data = rf_train, ntree = 100, mtry = 3, na.action = na.roughfix
  )
  rf_prob_mat <- predict(rf_model, newdata = rf_test, type = "prob")
  rf_prob <- if ("1" %in% colnames(rf_prob_mat)) rf_prob_mat[, "1"] else rf_prob_mat[, 2]
  rf_metrics <- eval_metrics(y_test, rf_prob)
  
  # Feature importance for Random Forest
  rf_imp <- randomForest::importance(rf_model)
  imp_df <- data.frame(feature = rownames(rf_imp), importance = round(unname(rf_imp[, 1]), 2))
  imp_df <- imp_df[order(-imp_df$importance), ]
  rf_importance_list <- lapply(1:min(12, nrow(imp_df)), function(i) {
    list(feature = as.character(imp_df$feature[i]), importance = as.numeric(imp_df$importance[i]))
  })
  
  # 4. XGBoost
  # One-hot encode for XGBoost
  x_train_mat <- model.matrix(fmla, data = train_df)[, -1]
  x_test_mat <- model.matrix(fmla, data = test_df)[, -1]
  
  dtrain <- xgboost::xgb.DMatrix(data = x_train_mat, label = train_df$target)
  dtest <- xgboost::xgb.DMatrix(data = x_test_mat, label = test_df$target)
  
  xgb_params <- list(
    objective = "binary:logistic",
    eval_metric = "auc",
    max_depth = 4,
    eta = 0.1,
    scale_pos_weight = sum(train_df$target == 0) / pmax(1, sum(train_df$target == 1))
  )
  xgb_model <- xgboost::xgb.train(params = xgb_params, data = dtrain, nrounds = 50, verbose = 0)
  xgb_prob <- predict(xgb_model, dtest)
  xgb_metrics <- eval_metrics(y_test, xgb_prob)
  
  # Best model selection by ROC-AUC
  all_aucs <- c(
    "Logistic Regression" = lr_metrics$auc,
    "Decision Tree" = dt_metrics$auc,
    "Random Forest" = rf_metrics$auc,
    "XGBoost" = xgb_metrics$auc
  )
  best_name <- names(which.max(all_aucs))
  
  # Pick best probability vector for saving
  best_probs <- switch(best_name,
    "Logistic Regression" = lr_prob,
    "Decision Tree" = dt_prob,
    "Random Forest" = rf_prob,
    "XGBoost" = xgb_prob
  )
  
  # Save predictions CSV for user download
  pred_export_df <- data.frame(
    session_id = test_df$session_id,
    session_start_time = as.character(test_df$session_start_time),
    actual_converted = test_df$target,
    predicted_probability = round(best_probs, 4),
    predicted_converted = as.integer(best_probs >= 0.5),
    best_model = best_name
  )
  data.table::fwrite(pred_export_df, file.path(s_path, "conversion_predictions.csv"))
  
  # Save best model and artifacts in RDS for reuse
  saveRDS(list(
    best_model_name = best_name,
    lr = lr_model,
    rpart = dt_model,
    rf = rf_model,
    xgb = xgb_model,
    test_df = test_df,
    best_probs = best_probs
  ), file.path(s_path, "conversion_models.rds"))
  
  return(list(
    cohort_summary = list(
      total_cohort_sessions = n_total,
      train_sessions = nrow(train_df),
      test_sessions = nrow(test_df),
      cohort_conversion_rate = round(mean(df$target) * 100, 2),
      majority_class_baseline_accuracy = majority_baseline_acc
    ),
    models = list(
      list(name = "Logistic Regression", metrics = lr_metrics),
      list(name = "Decision Tree", metrics = dt_metrics),
      list(name = "Random Forest", metrics = rf_metrics),
      list(name = "XGBoost", metrics = xgb_metrics)
    ),
    best_model = best_name,
    feature_importance = rf_importance_list
  ))
}
