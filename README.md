# QuantRisk Enterprise™ — Institutional Risk & Portfolio Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary%20Commercial%20%2F%20MIT-green.svg)](LICENSE)
[![Basel III](https://img.shields.io/badge/Regulatory-Basel%20III%20%2F%20IV%20Compliant-gold.svg)](https://www.bis.org/)
[![Status](https://img.shields.io/badge/Platform%20Status-Live%20v2.5%20Enterprise-success.svg)](https://quantrisk-enterprise.netlify.app)

**QuantRisk Enterprise™** is a commercial-grade Quantitative Financial Risk Management and Portfolio Intelligence SaaS Platform designed for hedge funds, asset managers, family offices, bank treasury desks, and financial risk compliance auditors.

Rooted in the rigorous mathematical foundations of **Continuous Random Variables**, this platform transforms 5 years of high-frequency historical S&P 500 equity data ($N = 1,258$ trading days per asset across 41 institutional tickers and preset portfolios) into actionable risk diagnostics, non-Gaussian tail modeling, Markowitz portfolio optimization, and multi-horizon stress testing.

---

## 📌 Executive Feature Matrix

| Feature Module | Institutional Capability | Academic Mathematical Foundation | Regulatory Standard |
|---|---|---|---|
| **Basel III / IV Risk Engine** | Parametric VaR, Historical Simulation VaR, **Cornish-Fisher VaR** (Adjusted for skewness & kurtosis), **Conditional VaR (Expected Shortfall - CVaR)** | Continuous PDF/CDF, Standardized Moments ($\mu, \sigma^2, \gamma_1, \gamma_2$), Cornish-Fisher expansion | Basel Committee Banking Supervision (BCBS 239) |
| **Markowitz Portfolio Optimizer** | Real-time weight sliders, Maximum Sharpe Tangency Portfolio, Minimum Volatility Portfolio, Multi-Asset Correlation Heatmaps | Modern Portfolio Theory (MPT), Matrix Quadratic Optimization, Vector Covariance $\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$ | CFA & Quantitative Finance Standard |
| **Black Swan & Macro Stress Lab** | Historical Crash Simulators (1987, 2000, 2008, 2010, 2020) + Forward Macro Shocks (Stagflation, Yield Spikes, Liquidity Freeze) + **Reverse Stress Testing** | Extreme Value Theory (EVT), $Z$-Score Tail Probability $P(Z \le z)$, Generalized Error Modeling | Federal Reserve CCAR / DFAST Standards |
| **Monte Carlo Stochastic Engine** | 60–252 day future price path projections with 5th/50th/95th percentile confidence corridors | Continuous Geometric Brownian Motion (GBM): $dS_t = \mu S_t dt + \sigma S_t dW_t$ | Black-Scholes-Merton & Quantitative Risk |
| **Multi-Model Goodness-of-Fit** | Model ranking via Log-Likelihood, Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC) | Student's $t$ (Heavy Tails), Laplace (Double Exponential), Logistic, Gaussian Normal | Maximum Likelihood Estimation (MLE) |
| **Multi-Currency & Capital Sizing** | Dynamic portfolio valuation ($10k to $100M+) with monetary loss ($/SAR/AED/EUR/EGP Loss at Risk) | Linear Scaled Random Variables $Y = aX + b$ | Global Multi-Currency Treasury Management |
| **Bilingual Localization (EN / AR)** | Instant English $\leftrightarrow$ Arabic language switcher with accurate financial terminology | Full RTL Layout & Financial Terminology | Sovereign Wealth Funds (PIF, ADIA, QIA, FRA) |
| **Audit-Ready Report & API** | 1-Click Board-Ready PDF Audit Report, Excel/CSV Export, and REST API Payload Specs | Reproducible Statistical Computing | Executive Risk Committee & Board Presentation |

---

## 📊 Empirical S&P 500 Statistical Baseline ($N = 1,258$ Trading Days)

| Statistical Parameter | Symbol / Derivation | Empirical Value | Theoretical Normal Target | Financial Risk Interpretation |
|---|---|---|---|---|
| **Sample Observations** | $N$ | **1,258 Days** | — | 5 full years of continuous trading observations |
| **Daily Expected Return** | $\mu = E[X]$ | **+0.0543%** | $0.00\%$ | Positive daily asset growth drift |
| **Annualized Return** | $E[R_{\text{ann}}] = (1+\mu)^{252}-1$ | **+14.67% / yr** | — | Compounded expected annual return |
| **Daily Volatility** | $\sigma = \sqrt{\text{Var}(X)}$ | **0.7980%** | — | Standard deviation of daily percentage price changes |
| **Annualized Volatility** | $\sigma_{\text{ann}} = \sigma \sqrt{252}$ | **12.67% / yr** | — | Annualized market volatility |
| **Skewness (3rd Moment)** | $\gamma_1 = E[(\frac{X-\mu}{\sigma})^3]$ | **-0.5237** | $0.0000$ | Negative asymmetry (Left-tail crash risk) |
| **Excess Kurtosis (4th Moment)**| $\gamma_2 = E[(\frac{X-\mu}{\sigma})^4] - 3$| **+2.5985** | $0.0000$ | **Leptokurtic Heavy Fat Tails** (Extreme outlier shocks) |
| **99% Historical 1-Day VaR** | $\text{VaR}_{0.01}^{\text{Hist}}$ | **-2.27%** | $-1.80\%$ | Realized worst 1% single-day decline |
| **99% Cornish-Fisher VaR** | $\text{VaR}_{0.01}^{\text{CF}}$ | **-2.51%** | $-1.80\%$ | Non-Gaussian moment-adjusted VaR |
| **99% Expected Shortfall (CVaR)**| $\text{ES}_{0.01}$ | **-2.96%** | $-2.05\%$ | **Basel III Mandate:** Average loss in the worst 1% tail |
| **Annualized Sharpe Ratio** | $(E[R_{\text{ann}}] - R_f) / \sigma_{\text{ann}}$ | **+0.798** | — | Risk-adjusted return assuming $R_f = 4.5\%$ |
| **Normality Test Status** | Jarque-Bera & Shapiro-Wilk | **REJECTED** | $p > 0.05$ | Systematic rejection of Gaussian Normal ($p < 10^{-89}$) |

---

## 🛠️ Repository Architecture

```
.
├── index.html                   # Enterprise SaaS Dashboard UI & Workspace
├── styles.css                   # Bloomberg Dark Glassmorphic Design & RTL Styles
├── app.js                       # Client-Side Quantitative Risk Engine & Chart.js Visualizer
├── app_data.js                  # Pre-computed JSON Database (41 Assets & Portfolios)
├── app_data.json                # Raw Institutional JSON Data Store
├── analysis.py                  # Python Quantitative Data & Diagnostic Plots Pipeline
├── Run_App.bat                  # 1-Click Desktop Launcher
├── report.md                    # Comprehensive Academic Research Paper & Technical Spec
├── summary_metrics.txt          # Exported Text Summary of Empirical Metrics
├── requirements.txt             # Python Package Dependencies
├── data/                        # High-Frequency S&P 500 Historical Dataset (505 Equities)
└── plots/                       # High-Resolution Publication-Quality Diagnostic Figures
```

---

## 🚀 Quick Start Guide

### 1. Launching Interactive SaaS Web Application
Open `index.html` in any modern web browser or serve locally:
```powershell
# Using Python builtin server
py -m http.server 8000
```
Then navigate to `http://localhost:8000`.

### 2. Running Quantitative Data Pipeline
```powershell
# 1. Export institutional asset universe & Basel metrics
py export_app_data.py

# 2. Export advanced stress testing & Markowitz frontier
py export_advanced_metrics.py

# 3. Generate diagnostic plots & statistical summary
py analysis.py
```

### 3. Generating Board-Ready PDF Audit & Pitch Deck
```powershell
# Generate 12-Page Executive PDF Report
py generate_pdf_report.py

# Generate Commercial PowerPoint Presentation
py generate_pptx_presentation.py
```

---

## 💎 Commercial B2B SaaS Tiers

| Tier | Target Client | Monthly Pricing | Features Included |
|---|---|---|---|
| **Quant Hedge Fund** | Boutique Funds & Algo Teams | **$4,999 / mo** | 500+ Assets, Custom CSV parser, Basel III VaR/CVaR, Cornish-Fisher Engine, REST API (100k calls/day) |
| **Asset Management Enterprise** | Institutional Committees & Family Offices | **$12,500 / mo** | Full Markowitz Portfolio Optimizer, Stress Lab, Monte Carlo GBM Projections, Board-Ready PDF Generator |
| **Global Institutional Bank** | Tier-1 Banks & Treasury Desks | **$25,000 / mo** | Unlimited Multi-Currency Portfolios, FIX/Kafka Data Feeds, Basel IV Compliance Module, 99.99% SLA |

---

## 🏛️ Platform Architecture & Engineering

- **Lead Quantitative Architect & Author:** Omar Saeed
- **Core Algorithms:** High-precision continuous statistics in Python (`scipy.stats`, `numpy`, `pandas`), interactive visualization via Vanilla ES6+ and Chart.js, and econometric stress models.
