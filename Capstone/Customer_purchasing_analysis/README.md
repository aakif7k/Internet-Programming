# Analysis of Customer Purchase Patterns and Conversion Prediction, Revenue Estimation, and Segmentation Using Website Clickstream Data

A full-stack, enterprise-grade Capstone Web Application built for an advanced R programming course. The application performs complete clickstream journey analysis, parametric & non-parametric exploratory data analysis, customer RFM segmentation via silhouette-evaluated k-means clustering, leakage-free session conversion prediction (Logistic Regression, Decision Trees, Random Forest, XGBoost), expected monetary revenue estimation, and ARIMA/ETS time-series forecasting.

---

## Architecture Overview

```
                      ┌───────────────────────────────────────────────┐
                      │    React 18 + TypeScript + Vite (:5173)       │
                      │  Tailwind CSS + Apache ECharts + React Router │
                      └───────────────────────┬───────────────────────┘
                                              │ HTTP / JSON
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │      Python FastAPI Orchestrator (:8000)       │
                      │  Session isolation, streaming upload, exports  │
                      └───────────────────────┬───────────────────────┘
                                              │ Internal Proxy
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │          R Analytics Plumber (:8001)          │
                      │   All statistics, feature engineering, models │
                      │  data.table, caret, randomForest, xgboost...  │
                      └───────────────────────────────────────────────┘
                                              │
                      ┌───────────────────────▼───────────────────────┐
                      │   Isolated Temp Session Storage (temp_sessions)│
                      │   raw_clickstream.csv / cleaned_clickstream.csv│
                      └───────────────────────────────────────────────┘
```

1. **R Analytics Engine (`r-analytics/` on port 8001)**:
   - Written strictly in R using `plumber`.
   - Performs **ALL** calculations, aggregations, feature transformations, econometric modeling, machine learning, and chart option generation.
   - Packages used: `plumber`, `data.table`, `dplyr`, `tidyr`, `jsonlite`, `caret`, `randomForest`, `xgboost`, `pROC`, `ggplot2`, `forecast`, `cluster`, `rpart`.
2. **FastAPI Orchestrator (`backend/` on port 8000)**:
   - Python FastAPI + Pydantic + Uvicorn.
   - **Zero analytics in Python** (no pandas). Dedicated solely to HTTP session management, HttpOnly cookies, streaming CSV upload validation, session expiry (8 hours), and safe proxying.
3. **React UI Frontend (`frontend/` on port 5173)**:
   - React 18, TypeScript, Tailwind CSS, Apache ECharts (`echarts-for-react`), Axios, React Router.
   - Features dark/light mode toggle, collapsible sidebar, responsive layout, exportable charts (PNG/SVG), CSV downloads.

---

## 12 Analytical Modules & Pages

1. **Overview**: Executive KPIs (total events, sessions, unique customers, conversion rate, gross revenue, AOV), daily trends, and event breakdowns.
2. **Dataset Upload & Field Mapping**: Drag-and-drop CSV upload, 50-row full table preview with horizontal scrolling, column schema & missing value audit, and auto-detected field mapping.
3. **Data Preprocessing**: Deduplication, POSIXct timestamp parsing, median/mode missing value imputation, and 3x IQR outlier clipping. Writes a separate `cleaned_clickstream.csv` without modifying the raw file.
4. **Exploratory Data Analysis (EDA)**: Descriptive statistics table (mean, SD, median, quartiles, missing counts), distribution histograms, Pearson correlation heatmap, and categorical cross-tabulations.
5. **Clickstream Analysis**: Page visit rankings, top 4-step navigation paths, Markov transition probability matrix, and bounce rate metrics.
6. **Purchase Patterns**: Viewed vs purchased product category comparison, average order value (AOV) by device and traffic source, hourly and day-of-week purchase patterns.
7. **Conversion Funnel**: Configurable stages (Browsing &rarr; Add to Cart &rarr; Checkout &rarr; Purchase), session drop-off numbers, step-to-step and overall conversion rates.
8. **Customer RFM Segmentation**: Recency, Frequency, Monetary scoring with silhouette analysis across $k=2$ to $k=6$, 2D PCA cluster projection, named segments, and CSV export.
9. **Conversion Prediction (R Machine Learning)**:
   - Strictly enforces leakage prevention: prediction cohort cut at first `add_to_cart` using only pre-cart browsing events.
   - 80/20 chronological train/test split.
   - Benchmarks Logistic Regression (`glm`), Decision Tree (`rpart`), Random Forest (`randomForest`), and XGBoost (`xgboost`) against the majority-class baseline.
   - Generates ROC curves, confusion matrices, Gini feature importance, and downloadable predictions CSV.
10. **Revenue Estimation**:
    - **Part A**: Order value regression for converted sessions using Linear Regression (`lm`), Random Forest, and XGBoost against a mean-prediction baseline.
    - **Part B**: Expected monetary value calculation: $\mathbb{E}[\text{Revenue}] = P(\text{Convert}) \times \widehat{\text{Order Value}}$, evaluated by device and traffic channel.
    - **Part C**: 30-day daily revenue forecast with confidence intervals.
11. **Time-Series Analysis & Forecasting**: Daily, weekly, and monthly metric tracking with automated ARIMA/ETS forecasting (`forecast` package) and 80%/95% prediction intervals.
12. **Visual Analytics Studio**: Dynamic chart builder supporting bar, grouped, stacked, line, area, pie, doughnut, scatter, funnel, treemap, and radar charts with custom SQL-style filters, aggregations, and CSV exports.

---

## First-Time Setup Instructions (Windows)

### 1. Prerequisites
- **R 4.x** installed (default path: `C:\Program Files\R\R-4.6.2\bin\Rscript.exe`)
- **Python 3.10+** installed
- **Node.js 18+** & npm installed

### 2. Install R Packages
Run the automated installation script:
```powershell
& "C:\Program Files\R\R-4.6.2\bin\Rscript.exe" scripts\setup_r_packages.R
```
This installs all 13 required R packages and their binary dependencies into `./r-library/`.

### 3. Setup Python Backend Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]" pydantic httpx python-multipart
```

### 4. Setup Frontend
```powershell
cd frontend
npm install
npm run build
cd ..
```

---

## How to Run the Application

### Option A: One-Command Runner
Launch all 3 services in separate windows and open the browser automatically:
```powershell
.\scripts\run_all.ps1
```

### Option B: Running Each Service Manually

**Terminal 1 — R Analytics (Port 8001):**
```powershell
.\scripts\run_r_analytics.ps1
```

**Terminal 2 — FastAPI Backend (Port 8000):**
```powershell
.\scripts\run_backend.ps1
```

**Terminal 3 — Frontend (Port 5173):**
```powershell
.\scripts\run_frontend.ps1
```

**Open your browser to:**
```
http://localhost:5173
```
Click **"Load Capstone Dataset"** in the top bar to instantly load the 10,000 session dataset into your session and explore all 12 modules.
