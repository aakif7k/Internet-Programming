# scripts/setup_r_packages.R: Installs all required R packages for the Capstone Web App

lib_dir <- normalizePath(file.path(getwd(), "r-library"), winslash = "/", mustWork = FALSE)
if (!dir.exists(lib_dir)) {
  dir.create(lib_dir, recursive = TRUE)
}

# Ensure .libPaths contains our project library first, plus base R library
base_r_lib <- file.path(R.home(), "library")
.libPaths(c(lib_dir, base_r_lib))

packages <- c(
  "plumber",
  "data.table",
  "dplyr",
  "tidyr",
  "jsonlite",
  "caret",
  "randomForest",
  "xgboost",
  "pROC",
  "ggplot2",
  "forecast",
  "cluster",
  "rpart"
)

cat("Target library directory:", lib_dir, "\n")
cat("Checking installed packages...\n")

installed <- character(0)
tryCatch({
  inst_mat <- installed.packages(lib.loc = c(lib_dir, base_r_lib))
  installed <- inst_mat[, "Package"]
}, error = function(e) {
  cat("Note on installed check:", e$message, "\n")
})

missing_pkgs <- setdiff(packages, installed)

if (length(missing_pkgs) > 0) {
  cat("Installing missing packages:", paste(missing_pkgs, collapse = ", "), "\n")
  install.packages(
    missing_pkgs,
    lib = lib_dir,
    repos = "https://cloud.r-project.org",
    type = "binary",
    dependencies = TRUE
  )
} else {
  cat("All required R packages are already installed!\n")
}

cat("\nVerifying package loading:\n")
all_good <- TRUE
for (pkg in packages) {
  ok <- suppressPackageStartupMessages(require(pkg, character.only = TRUE, quietly = TRUE, lib.loc = c(lib_dir, base_r_lib)))
  cat(sprintf("  %-15s : %s\n", pkg, ifelse(ok, "OK", "FAILED")))
  if (!ok) all_good <- FALSE
}

if (!all_good) {
  stop("One or more packages failed to load.")
} else {
  cat("\nSUCCESS: All 13 packages loaded successfully!\n")
}
