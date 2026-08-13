# MAT231 Project: Continuous Random Variables & S&P 500 Return Analysis

[![MAT231](https://img.shields.io/badge/Course-MAT231%20Probability%20%26%20Statistics-blue.svg)](https://github.com/Omarsaeed10/MAT231-Project)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An in-depth statistical and financial analysis modeling daily percentage stock market returns as **Continuous Random Variables**. This project utilizes 5 years of historical S&P 500 data ($N = 1,258$ trading days) to calculate empirical statistical moments, perform inferential confidence interval estimation, execute normality diagnostic tests, simulate Black Swan tail-risk events, and provide an interactive web dashboard.

---

## 📌 Project Highlights & Core Features

- **Mathematical Foundations**: Comprehensive derivation of Continuous Random Variable PDF/CDF, Standardized Moments, and Chi-Square / Normal Confidence Intervals.
- **Empirical Market Diagnostics**: Analysis of S&P 500 daily market returns proving negative skewness ($\gamma_1 = -0.5237$) and leptokurtic fat tails ($\gamma_2 = +2.5985$).
- **Normality Tests**: Rejection of Gaussian Normality via Jarque-Bera ($p = 4.53 \times 10^{-90}$) and Shapiro-Wilk ($p = 7.00 \times 10^{-17}$) tests.
- **Real-World Risk Metrics**: 95% & 99% Value at Risk (VaR), stress testing against 1987 Black Monday, 2008 Financial Crisis, and 2020 COVID Flash Crash.
- **Multi-Model Fitting**: Distribution goodness-of-fit ranking (Student's $t$-Distribution #1, Laplace #2, Logistic #3, Gaussian Normal #4).
- **Interactive Web App**: Fully dynamic web interface with live Chart.js visualization, distribution model comparison, interactive VaR calculator, and stress simulators.

---

## 📊 Empirical Statistical Summary ($N = 1,258$ Trading Days)

| Statistical Metric | Symbol / Formula | Empirical Value | Theoretical Normal Target | Financial Interpretation |
|---|---|---|---|---|
| **Sample Size** | $N$ | **1,258** | — | 5 years of daily market observations |
| **Mean Daily Return** | $\mu = E[X]$ | **+0.0543%** | $0.00\%$ | Expected positive daily growth |
| **Variance** | $\sigma^2$ | **0.00006369** | — | Measure of return dispersion |
| **Standard Deviation** | $\sigma$ | **0.7980%** | — | Daily market volatility |
| **Skewness** | $\gamma_1$ | **-0.5237** | $0.0000$ | Asymmetric left-tailed crash risk |
| **Excess Kurtosis** | $\gamma_2$ | **+2.5985** | $0.0000$ | High Leptokurtosis (Fat tails / Outliers) |
| **Minimum Return** | $X_{\min}$ | **-4.13%** | Symmetric | Maximum 1-day decline |
| **Maximum Return** | $X_{\max}$ | **+3.24%** | Symmetric | Maximum 1-day gain |
| **Median Return** | $\tilde{X}$ | **+0.0797%** | $\approx \mu$ | 50th percentile of market returns |
| **Standard Error** | $SE(\bar{X})$ | **0.0225%** | — | Mean sampling error |
| **95% CI for Mean** | $\mu \in [\text{Lower}, \text{Upper}]$ | **[+0.0102%, +0.0984%]** | — | Population expected return boundary |
| **95% CI for Variance** | $\sigma^2 \in [\text{Lower}, \text{Upper}]$ | **[0.0000592, 0.0000687]** | — | Population variance boundary ($\chi^2$) |

---

## 💥 Black Swan Crises Stress Simulator

Testing historical market crashes against theoretical Gaussian Normal predictions ($Z = \frac{X - \mu}{\sigma}$):

| Historical Crash Event | Date | 1-Day Drop | Theoretical $Z$-Score | Gaussian Predicted Odds | Empirical Reality |
|---|---|---|---|---|---|
| **1987 Black Monday** | Oct 19, 1987 | **-20.47%** | $Z = -25.72$ | $1 \text{ in } 10^{145} \text{ Universes}$ | Realized Historic Fact |
| **2008 Lehman Brothers** | Sep 29, 2008 | **-8.81%** | $Z = -11.11$ | $1 \text{ in } 1.4 \text{ Billion Years}$ | Realized Historic Fact |
| **2020 COVID Flash Crash** | Mar 16, 2020 | **-11.98%** | $Z = -15.08$ | $1 \text{ in } 10^{31} \text{ Years}$ | Realized Historic Fact |

---

## 📈 Visualizations

The project generates high-resolution analytical plots stored in `plots/`:

- **Histogram & PDF**: Empirical density vs fitted Gaussian curve.
- **Q-Q Plot**: Quantile-Quantile diagnostic highlighting heavy-tail deviations.
- **Time Series**: Daily returns timeline showing volatility clustering.
- **Boxplot**: Outlier detection extending beyond standard whisker bounds.
- **CDF Comparison**: Empirical Cumulative Distribution Function vs Normal CDF.

---

## 📁 Repository Structure

```
.
├── index.html                   # Main interactive Web Application UI
├── styles.css                   # Web Application styling & modern design system
├── app.js                       # Interactive dashboard logic & Chart.js rendering
├── app_data.js                  # Pre-processed JSON dataset for web interface
├── analysis.py                  # Python statistical computing & analysis script
├── analysis.R                   # R statistical computing & analysis script
├── compute_stats.py             # Helper script for moments and hypothesis tests
├── export_app_data.py           # Exporter script generating web data artifacts
├── export_advanced_metrics.py   # Exporter script for advanced risk & tail metrics
├── report.md                    # Full academic research paper and theoretical report
├── requirements.txt             # Python dependencies
├── data/                        # S&P 500 historical dataset directory
└── plots/                       # Generated high-resolution diagnostic plots
```

---

## 🚀 Quick Start & Usage

### 1. Interactive Web Application
To run the web application locally, simply open `index.html` in any modern web browser or serve via a local server:

```bash
# Using Python builtin HTTP server
python -m http.server 8000
```
Then visit `http://localhost:8000`.

### 2. Python Statistical Analysis
Install required dependencies and execute the Python analysis pipeline:

```bash
pip install -r requirements.txt
python analysis.py
```

### 3. R Statistical Analysis
Execute the R script in R or RStudio:

```bash
Rscript analysis.R
```

---

## 🛠️ Built With

- **Python**: `pandas`, `scipy`, `numpy`, `matplotlib`, `seaborn`
- **R**: `ggplot2`, `moments`, `dplyr`
- **Web Frontend**: HTML5, Vanilla CSS3, JavaScript (ES6+), Chart.js, MathJax

---

## 🎓 Course & Author Info

- **Course**: MAT231 — Probability & Statistics
- **Topic**: Continuous Random Variables — Financial Statistics Analysis
- **Author**: Omarsaeed10
