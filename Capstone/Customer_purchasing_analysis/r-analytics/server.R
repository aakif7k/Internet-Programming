# server.R: Launches Plumber on port 8001
# Ensure project r-library is in .libPaths
base_dir <- normalizePath(file.path(getwd(), ".."), winslash = "/", mustWork = FALSE)
lib_dir <- file.path(base_dir, "r-library")
if (!dir.exists(lib_dir)) {
  lib_dir <- normalizePath(file.path(getwd(), "r-library"), winslash = "/", mustWork = FALSE)
}
if (dir.exists(lib_dir)) {
  .libPaths(c(lib_dir, .libPaths()))
}

suppressPackageStartupMessages({
  library(plumber)
})

cat("R library paths:\n")
print(.libPaths())
cat("Starting R Plumber Analytics Service on port 8001...\n")

pr <- plumber::plumb("plumber.R")
pr$run(host = "127.0.0.1", port = 8001)
