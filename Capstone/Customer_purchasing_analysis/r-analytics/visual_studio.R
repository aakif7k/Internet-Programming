# visual_studio.R: Dynamic query engine and Apache ECharts option generator
suppressPackageStartupMessages({
  library(data.table)
  library(jsonlite)
})
source("utils.R")

query_visual_studio <- function(session_id, config) {
  dt <- load_session_data(session_id)
  s_path <- get_session_path(session_id)
  
  chart_type <- ifelse(is.null(config$chart_type), "bar", as.character(config$chart_type))
  x_col <- config$x_col
  y_col <- config$y_col
  group_col <- config$group_col
  agg_func <- ifelse(is.null(config$agg_func), "count", as.character(config$agg_func)) # sum, mean, count, distinct_count, min, max, median
  filters <- config$filters
  sort_order <- ifelse(is.null(config$sort_order), "desc", as.character(config$sort_order))
  limit <- ifelse(is.null(config$limit), 30, as.integer(config$limit))
  
  # Apply filters
  if (!is.null(filters) && length(filters) > 0) {
    for (f in filters) {
      col <- f$column
      op <- f$operator
      val <- f$value
      if (!is.null(col) && col %in% names(dt) && !is.null(val) && val != "") {
        if (op == "=") {
          dt <- dt[get(col) == val]
        } else if (op == "!=") {
          dt <- dt[get(col) != val]
        } else if (op == ">") {
          dt <- dt[get(col) > as.numeric(val)]
        } else if (op == "<") {
          dt <- dt[get(col) < as.numeric(val)]
        } else if (op == ">=") {
          dt <- dt[get(col) >= as.numeric(val)]
        } else if (op == "<=") {
          dt <- dt[get(col) <= as.numeric(val)]
        } else if (op == "contains") {
          dt <- dt[grepl(val, as.character(get(col)), ignore.case = TRUE)]
        }
      }
    }
  }
  
  if (nrow(dt) == 0) {
    return(list(status = "empty", message = "No records match the selected filters."))
  }
  
  # Validation of X column
  if (is.null(x_col) || !x_col %in% names(dt)) {
    x_col <- if ("event_type" %in% names(dt)) "event_type" else names(dt)[1]
  }
  
  # Helper aggregation expression using bquote
  get_agg_expr <- function(cname, func) {
    sym <- as.name(cname)
    if (func == "sum") return(bquote(sum(.(sym), na.rm = TRUE)))
    if (func == "mean") return(bquote(round(mean(.(sym), na.rm = TRUE), 2)))
    if (func == "min") return(bquote(min(.(sym), na.rm = TRUE)))
    if (func == "max") return(bquote(max(.(sym), na.rm = TRUE)))
    if (func == "median") return(bquote(median(.(sym), na.rm = TRUE)))
    if (func == "distinct_count") return(bquote(data.table::uniqueN(.(sym))))
    return(quote(.N)) # count
  }
  
  # Check if grouping is active
  has_group <- !is.null(group_col) && group_col != "" && group_col %in% names(dt) && group_col != x_col
  
  # Build aggregated table
  agg_dt <- NULL
  if (chart_type %in% c("scatter", "box")) {
    # Non-aggregated raw sample points
    sample_rows <- min(nrow(dt), 800)
    sub_dt <- dt[sample(.N, sample_rows)]
    
    if (chart_type == "scatter") {
      y_axis_col <- if (!is.null(y_col) && y_col %in% names(dt)) y_col else names(dt)[sapply(dt, is.numeric)][1]
      clean_scatter <- na.omit(sub_dt[, c(x_col, y_axis_col), with = FALSE])
      data_points <- lapply(1:nrow(clean_scatter), function(i) {
        list(as.numeric(clean_scatter[[x_col]][i]), as.numeric(clean_scatter[[y_axis_col]][i]))
      })
      echarts_option <- list(
        tooltip = list(trigger = "item"),
        xAxis = list(type = "value", name = x_col),
        yAxis = list(type = "value", name = y_axis_col),
        series = list(list(type = "scatter", data = data_points, symbolSize = 8))
      )
      return(list(status = "ok", echarts_option = echarts_option, row_count = nrow(clean_scatter)))
    }
  }
  
  # Grouped or Single Aggregation
  by_cols <- if (has_group) c(x_col, group_col) else x_col
  
  if (agg_func == "count" || is.null(y_col) || !y_col %in% names(dt)) {
    agg_dt <- dt[, .(metric_val = .N), by = by_cols]
  } else {
    expr <- get_agg_expr(y_col, agg_func)
    agg_dt <- dt[, .(metric_val = eval(expr)), by = by_cols]
  }
  
  # Fill NA values
  agg_dt[is.na(metric_val), metric_val := 0]
  
  # Sort
  if (sort_order == "desc") {
    data.table::setorder(agg_dt, -metric_val)
  } else {
    data.table::setorder(agg_dt, metric_val)
  }
  
  # Save aggregated CSV for export
  export_path <- file.path(s_path, "dynamic_chart_export.csv")
  data.table::fwrite(agg_dt, export_path)
  
  # Build ECharts Option based on chart_type
  echarts_option <- list()
  
  if (chart_type %in% c("bar", "grouped", "stacked", "line", "area")) {
    if (!has_group) {
      top_dt <- head(agg_dt, limit)
      x_vals <- as.character(top_dt[[x_col]])
      y_vals <- as.numeric(top_dt$metric_val)
      
      series_def <- list(
        name = ifelse(is.null(y_col), agg_func, paste0(agg_func, "(", y_col, ")")),
        type = ifelse(chart_type == "bar", "bar", "line"),
        data = y_vals
      )
      if (chart_type == "area") {
        series_def$areaStyle <- list(opacity = 0.4)
        series_def$smooth <- TRUE
      }
      
      echarts_option <- list(
        tooltip = list(trigger = "axis"),
        xAxis = list(type = "category", data = x_vals, axisLabel = list(rotate = 30, interval = 0)),
        yAxis = list(type = "value"),
        series = list(series_def)
      )
    } else {
      # Grouped or Stacked Bar/Line
      top_x <- head(unique(agg_dt[[x_col]]), limit)
      top_groups <- head(unique(agg_dt[[group_col]]), 8)
      
      sub_agg <- agg_dt[get(x_col) %in% top_x & get(group_col) %in% top_groups]
      series_list <- list()
      
      for (g in top_groups) {
        g_data <- sub_agg[get(group_col) == g]
        # Align with top_x
        val_map <- setNames(g_data$metric_val, as.character(g_data[[x_col]]))
        vals <- sapply(top_x, function(x) ifelse(as.character(x) %in% names(val_map), as.numeric(val_map[[as.character(x)]]), 0))
        
        s_obj <- list(
          name = as.character(g),
          type = ifelse(chart_type %in% c("line", "area"), "line", "bar"),
          data = unname(vals)
        )
        if (chart_type == "stacked") {
          s_obj$stack = "total"
        }
        if (chart_type == "area") {
          s_obj$areaStyle <- list(opacity = 0.3)
          s_obj$smooth <- TRUE
        }
        series_list[[length(series_list) + 1]] <- s_obj
      }
      
      echarts_option <- list(
        tooltip = list(trigger = "axis"),
        legend = list(data = as.character(top_groups)),
        xAxis = list(type = "category", data = as.character(top_x), axisLabel = list(rotate = 30)),
        yAxis = list(type = "value"),
        series = series_list
      )
    }
  } else if (chart_type %in% c("pie", "doughnut")) {
    top_dt <- head(agg_dt, limit)
    pie_data <- lapply(1:nrow(top_dt), function(i) {
      list(name = as.character(top_dt[[x_col]][i]), value = as.numeric(top_dt$metric_val[i]))
    })
    
    radius_val <- if (chart_type == "doughnut") c("40%", "70%") else "65%"
    echarts_option <- list(
      tooltip = list(trigger = "item", formatter = "{b}: {c} ({d}%)"),
      legend = list(orient = "vertical", left = "left", type = "scroll"),
      series = list(
        list(
          type = "pie",
          radius = radius_val,
          avoidLabelOverlap = TRUE,
          itemStyle = list(borderRadius = 6, borderColor = "#fff", borderWidth = 2),
          data = pie_data
        )
      )
    )
  } else if (chart_type == "treemap") {
    top_dt <- head(agg_dt, limit)
    tree_data <- lapply(1:nrow(top_dt), function(i) {
      list(name = as.character(top_dt[[x_col]][i]), value = as.numeric(top_dt$metric_val[i]))
    })
    echarts_option <- list(
      tooltip = list(trigger = "item"),
      series = list(
        list(type = "treemap", data = tree_data, label = list(show = TRUE, formatter = "{b}\n{c}"))
      )
    )
  } else if (chart_type == "funnel") {
    top_dt <- head(agg_dt, min(limit, 10))
    funnel_data <- lapply(1:nrow(top_dt), function(i) {
      list(name = as.character(top_dt[[x_col]][i]), value = as.numeric(top_dt$metric_val[i]))
    })
    echarts_option <- list(
      tooltip = list(trigger = "item", formatter = "{a} <br/>{b} : {c}"),
      series = list(
        list(type = "funnel", left = "10%", top = 40, bottom = 40, width = "80%", sort = "descending", gap = 2, data = funnel_data)
      )
    )
  } else if (chart_type == "radar") {
    top_dt <- head(agg_dt, min(limit, 8))
    max_val <- max(top_dt$metric_val, na.rm = TRUE) * 1.15
    indicators <- lapply(1:nrow(top_dt), function(i) {
      list(name = as.character(top_dt[[x_col]][i]), max = max_val)
    })
    radar_vals <- as.numeric(top_dt$metric_val)
    echarts_option <- list(
      tooltip = list(trigger = "item"),
      radar = list(indicator = indicators),
      series = list(
        list(type = "radar", data = list(list(value = radar_vals, name = ifelse(is.null(y_col), "Count", y_col))))
      )
    )
  }
  
  return(list(
    status = "ok",
    chart_type = chart_type,
    echarts_option = echarts_option,
    total_aggregated_rows = nrow(agg_dt),
    x_column = x_col,
    y_column = y_col,
    aggregation = agg_func
  ))
}

save_studio_config <- function(session_id, config_obj) {
  s_path <- get_session_path(session_id)
  cfg_file <- file.path(s_path, "studio_configs.json")
  existing <- list()
  if (file.exists(cfg_file)) {
    existing <- tryCatch(jsonlite::fromJSON(cfg_file, simplifyVector = FALSE), error = function(e) list())
  }
  existing[[length(existing) + 1]] <- config_obj
  jsonlite::write_json(existing, cfg_file, auto_unbox = TRUE, pretty = TRUE)
  return(list(status = "success", count = length(existing)))
}

get_studio_configs <- function(session_id) {
  s_path <- get_session_path(session_id)
  cfg_file <- file.path(s_path, "studio_configs.json")
  if (file.exists(cfg_file)) {
    return(jsonlite::fromJSON(cfg_file, simplifyVector = FALSE))
  }
  return(list())
}
