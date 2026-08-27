import pandas as pd
import numpy as np
import scipy.stats as stats
import json
import os

print("=" * 75)
print("QuantRisk Enterprise™: Universal 505-Asset Quantitative Pipeline")
print("=" * 75)

# 1. Load Dataset
data_path = os.path.join("data", "all_stocks_5yr.csv")
df = pd.read_csv(data_path)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Name', 'date'])

# Calculate Daily Returns
df['daily_return'] = df.groupby('Name')['close'].pct_change()
df_clean = df.dropna(subset=['daily_return']).copy()

# Market Returns Benchmark (Equal-weighted 500 stocks)
market_df = df_clean.groupby('date')['daily_return'].mean().reset_index()
market_df.columns = ['date', 'return']
market_df = market_df.sort_values('date')
market_returns = market_df['return'].values

RF_ANNUAL = 0.045
RF_DAILY = RF_ANNUAL / 252.0

# Top Institutional Equities & Portfolios Metadata
ASSET_METADATA = {
    'MARKET_AVG': {'name': 'S&P 500 Benchmark (Equal-Weighted Index)', 'sector': 'Market Benchmark', 'category': 'benchmark'},
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    'MSFT': {'name': 'Microsoft Corp.', 'sector': 'Technology & AI', 'category': 'equity'},
    'NVDA': {'name': 'NVIDIA Corp.', 'sector': 'Technology & AI', 'category': 'equity'},
    'GOOGL': {'name': 'Alphabet Inc. (Class A)', 'sector': 'Technology & AI', 'category': 'equity'},
    'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    'META': {'name': 'Meta Platforms Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    'ADBE': {'name': 'Adobe Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    'INTC': {'name': 'Intel Corp.', 'sector': 'Technology & AI', 'category': 'equity'},
    'CSCO': {'name': 'Cisco Systems Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    'CRM': {'name': 'Salesforce Inc.', 'sector': 'Technology & AI', 'category': 'equity'},
    
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Financials & Banking', 'category': 'equity'},
    'BAC': {'name': 'Bank of America Corp.', 'sector': 'Financials & Banking', 'category': 'equity'},
    'GS': {'name': 'Goldman Sachs Group Inc.', 'sector': 'Financials & Banking', 'category': 'equity'},
    'MS': {'name': 'Morgan Stanley', 'sector': 'Financials & Banking', 'category': 'equity'},
    'WFC': {'name': 'Wells Fargo & Co.', 'sector': 'Financials & Banking', 'category': 'equity'},
    'C': {'name': 'Citigroup Inc.', 'sector': 'Financials & Banking', 'category': 'equity'},
    
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    'UNH': {'name': 'UnitedHealth Group Inc.', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    'PFE': {'name': 'Pfizer Inc.', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    'ABBV': {'name': 'AbbVie Inc.', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    'ABT': {'name': 'Abbott Laboratories', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    'MRK': {'name': 'Merck & Co. Inc.', 'sector': 'Healthcare & Pharma', 'category': 'equity'},
    
    'XOM': {'name': 'Exxon Mobil Corp.', 'sector': 'Energy & Commodities', 'category': 'equity'},
    'CVX': {'name': 'Chevron Corp.', 'sector': 'Energy & Commodities', 'category': 'equity'},
    'COP': {'name': 'ConocoPhillips', 'sector': 'Energy & Commodities', 'category': 'equity'},
    'SLB': {'name': 'Schlumberger Ltd.', 'sector': 'Energy & Commodities', 'category': 'equity'},
    
    'BA': {'name': 'Boeing Co.', 'sector': 'Industrials & Aerospace', 'category': 'equity'},
    'CAT': {'name': 'Caterpillar Inc.', 'sector': 'Industrials & Aerospace', 'category': 'equity'},
    'GE': {'name': 'General Electric Co.', 'sector': 'Industrials & Aerospace', 'category': 'equity'},
    'HON': {'name': 'Honeywell International', 'sector': 'Industrials & Aerospace', 'category': 'equity'},
    
    'PG': {'name': 'Procter & Gamble Co.', 'sector': 'Consumer Staples & Retail', 'category': 'equity'},
    'KO': {'name': 'The Coca-Cola Company', 'sector': 'Consumer Staples & Retail', 'category': 'equity'},
    'PEP': {'name': 'PepsiCo Inc.', 'sector': 'Consumer Staples & Retail', 'category': 'equity'},
    'WMT': {'name': 'Walmart Inc.', 'sector': 'Consumer Staples & Retail', 'category': 'equity'},
    'MCD': {'name': "McDonald's Corp.", 'sector': 'Consumer Staples & Retail', 'category': 'equity'},
    'DIS': {'name': 'The Walt Disney Company', 'sector': 'Consumer & Entertainment', 'category': 'equity'}
}

def compute_asset_series(ticker):
    if ticker == 'MARKET_AVG':
        return market_df.copy()
    else:
        sub = df_clean[df_clean['Name'] == ticker][['date', 'daily_return']].copy()
        sub.columns = ['date', 'return']
        sub = sub.sort_values('date')
        return sub

def compute_institutional_stats(ret_series, dates_series, benchmark_returns):
    ret = np.array(ret_series)
    n = len(ret)
    
    mean_val = float(np.mean(ret))
    var_val = float(np.var(ret, ddof=1))
    std_val = float(np.std(ret, ddof=1))
    skew_val = float(stats.skew(ret))
    kurt_val = float(stats.kurtosis(ret))
    min_val = float(np.min(ret))
    max_val = float(np.max(ret))
    median_val = float(np.median(ret))
    q25, q75 = [float(x) for x in np.percentile(ret, [25, 75])]
    iqr_val = q75 - q25
    
    ann_mean = float(((1.0 + mean_val) ** 252) - 1.0)
    ann_std = float(std_val * np.sqrt(252))
    
    se_mean = float(std_val / np.sqrt(n))
    z_95 = 1.95996
    z_99 = 2.57583
    ci_mean_95 = [float(mean_val - z_95 * se_mean), float(mean_val + z_95 * se_mean)]
    ci_mean_99 = [float(mean_val - z_99 * se_mean), float(mean_val + z_99 * se_mean)]
    
    df_freedom = n - 1
    chi2_lower = stats.chi2.ppf(0.025, df_freedom)
    chi2_upper = stats.chi2.ppf(0.975, df_freedom)
    ci_var_95 = [float((df_freedom * var_val) / chi2_upper), float((df_freedom * var_val) / chi2_lower)]
    
    jb_stat, jb_p = [float(x) for x in stats.jarque_bera(ret)]
    sample_for_shapiro = ret[:5000] if len(ret) > 5000 else ret
    shapiro_stat, shapiro_p = [float(x) for x in stats.shapiro(sample_for_shapiro)]
    ks_stat, ks_p = [float(x) for x in stats.kstest(ret, 'norm', args=(mean_val, std_val))]
    
    # Basel III VaR
    var_hist_95 = float(np.percentile(ret * 100, 5))
    var_hist_99 = float(np.percentile(ret * 100, 1))
    var_hist_999 = float(np.percentile(ret * 100, 0.1))
    
    var_norm_95 = float((mean_val * 100) - 1.64485 * (std_val * 100))
    var_norm_99 = float((mean_val * 100) - 2.32635 * (std_val * 100))
    var_norm_999 = float((mean_val * 100) - 3.09023 * (std_val * 100))
    
    # Cornish Fisher
    def get_cf_quantile(alpha):
        z = stats.norm.ppf(alpha)
        s = skew_val
        k = kurt_val
        z_cf = z + (1.0/6.0)*(z**2 - 1.0)*s + (1.0/24.0)*(z**3 - 3.0*z)*k - (1.0/36.0)*(2.0*z**3 - 5.0*z)*(s**2)
        return float((mean_val * 100) + z_cf * (std_val * 100))
    
    var_cf_95 = get_cf_quantile(0.05)
    var_cf_99 = get_cf_quantile(0.01)
    
    # Conditional VaR (Expected Shortfall)
    tail_returns_95 = (ret * 100)[ret * 100 <= var_hist_95]
    cvar_hist_95 = float(np.mean(tail_returns_95)) if len(tail_returns_95) > 0 else var_hist_95
    
    tail_returns_99 = (ret * 100)[ret * 100 <= var_hist_99]
    cvar_hist_99 = float(np.mean(tail_returns_99)) if len(tail_returns_99) > 0 else var_hist_99
    
    # Multi-Horizon VaR Term Structure (1d, 5d, 10d Basel, 21d Month, 252d Year)
    # Using Square Root of Time rule: VaR(T) = VaR(1d) * sqrt(T)
    var_term_structure = {
        "1d_99": round(var_hist_99, 2),
        "5d_99": round(var_hist_99 * np.sqrt(5), 2),
        "10d_basel_99": round(var_hist_99 * np.sqrt(10), 2),
        "21d_month_99": round(var_hist_99 * np.sqrt(21), 2),
        "252d_year_99": round(var_hist_99 * np.sqrt(252), 2)
    }
    
    # Performance Ratios
    excess_annual_return = ann_mean - RF_ANNUAL
    sharpe_ratio = float(excess_annual_return / ann_std) if ann_std > 0 else 0.0
    
    downside_diffs = np.minimum(ret - RF_DAILY, 0.0)
    downside_dev_annual = float(np.sqrt(np.mean(downside_diffs**2)) * np.sqrt(252))
    sortino_ratio = float(excess_annual_return / downside_dev_annual) if downside_dev_annual > 0 else 0.0
    
    if len(benchmark_returns) == len(ret):
        cov_matrix = np.cov(ret, benchmark_returns)
        asset_beta = float(cov_matrix[0, 1] / cov_matrix[1, 1]) if cov_matrix[1, 1] > 0 else 1.0
    else:
        asset_beta = 1.0
    
    treynor_ratio = float(excess_annual_return / asset_beta) if asset_beta != 0 else 0.0
    
    cum_wealth = 100.0 * np.cumprod(1.0 + ret)
    cum_wealth = np.insert(cum_wealth, 0, 100.0)
    running_max = np.maximum.accumulate(cum_wealth)
    drawdowns = (cum_wealth - running_max) / running_max
    max_drawdown = float(np.min(drawdowns) * 100.0)
    
    decay_lambda = 0.94
    ewma_var = var_val
    for r in ret:
        ewma_var = decay_lambda * ewma_var + (1.0 - decay_lambda) * (r ** 2)
    ewma_daily_vol_pct = float(np.sqrt(ewma_var) * 100.0)
    ewma_annual_vol_pct = float(np.sqrt(ewma_var * 252.0) * 100.0)
    
    # Histogram & Fits
    counts, bin_edges = np.histogram(ret * 100, bins=60, density=True)
    bin_centers = [(bin_edges[i] + bin_edges[i+1])/2.0 for i in range(len(counts))]
    
    norm_pdf = [float(stats.norm.pdf(x, loc=mean_val*100, scale=std_val*100)) for x in bin_centers]
    
    try:
        t_params = stats.t.fit(ret * 100)
        t_pdf = [float(stats.t.pdf(x, *t_params)) for x in bin_centers]
        t_df = float(t_params[0])
    except Exception:
        t_pdf = norm_pdf
        t_df = 30.0
        
    try:
        laplace_params = stats.laplace.fit(ret * 100)
        laplace_pdf = [float(stats.laplace.pdf(x, *laplace_params)) for x in bin_centers]
    except Exception:
        laplace_pdf = norm_pdf
        
    try:
        logistic_params = stats.logistic.fit(ret * 100)
        logistic_pdf = [float(stats.logistic.pdf(x, *logistic_params)) for x in bin_centers]
    except Exception:
        logistic_pdf = norm_pdf
    
    res = stats.probplot(ret, dist="norm")
    step_qq = max(1, int(len(ret)/120))
    qq_theoretical = [float(x) for x in res[0][0][::step_qq]]
    qq_sample = [float(x) for x in res[0][1][::step_qq]]
    
    sorted_ret = np.sort(ret * 100)
    step_cdf = max(1, int(len(sorted_ret) / 120))
    cdf_x = [float(x) for x in sorted_ret[::step_cdf]]
    cdf_empirical = [float((i*step_cdf + 1) / len(sorted_ret)) for i in range(len(cdf_x))]
    cdf_normal_vals = [float(stats.norm.cdf(x, loc=mean_val*100, scale=std_val*100)) for x in cdf_x]
    
    date_strs = [pd.to_datetime(d).strftime('%Y-%m-%d') for d in dates_series]
    ret_pct = [round(float(r * 100.0), 3) for r in ret]
    
    series_ret = pd.Series(ret)
    rolling_vol_30d = series_ret.rolling(window=30).std() * np.sqrt(252.0) * 100.0
    rolling_vol_30d = rolling_vol_30d.bfill().fillna(0.0).values
    rolling_vol_clean = [round(float(v), 2) for v in rolling_vol_30d]
    
    step_ts = 2
    ts_dates = date_strs[::step_ts]
    ts_returns = ret_pct[::step_ts]
    ts_rolling_vol = rolling_vol_clean[::step_ts]
    ts_drawdowns = [round(float(d * 100.0), 2) for d in drawdowns[1:][::step_ts]]
    ts_cum_wealth = [round(float(w), 2) for w in cum_wealth[1:][::step_ts]]
    
    return {
        "n": n,
        "mean": mean_val,
        "mean_annual": ann_mean,
        "variance": var_val,
        "std": std_val,
        "std_annual": ann_std,
        "skewness": skew_val,
        "kurtosis": kurt_val,
        "min": min_val,
        "max": max_val,
        "median": median_val,
        "q25": q25,
        "q75": q75,
        "iqr": iqr_val,
        
        "jb_stat": jb_stat,
        "jb_p": jb_p,
        "shapiro_stat": shapiro_stat,
        "shapiro_p": shapiro_p,
        "ks_stat": ks_stat,
        "ks_p": ks_p,
        
        "var_metrics": {
            "hist_95": round(var_hist_95, 3),
            "hist_99": round(var_hist_99, 3),
            "hist_99_9": round(var_hist_999, 3),
            "norm_95": round(var_norm_95, 3),
            "norm_99": round(var_norm_99, 3),
            "norm_99_9": round(var_norm_999, 3),
            "cf_95": round(var_cf_95, 3),
            "cf_99": round(var_cf_99, 3),
            "cvar_hist_95": round(cvar_hist_95, 3),
            "cvar_hist_99": round(cvar_hist_99, 3),
            "term_structure": var_term_structure
        },
        
        "performance_metrics": {
            "sharpe_ratio": round(sharpe_ratio, 3),
            "sortino_ratio": round(sortino_ratio, 3),
            "beta": round(asset_beta, 3),
            "treynor_ratio": round(treynor_ratio, 3),
            "max_drawdown": round(max_drawdown, 2),
            "ewma_vol_daily": round(ewma_daily_vol_pct, 3),
            "ewma_vol_annual": round(ewma_annual_vol_pct, 2)
        },
        
        "lecture_metrics": {
            "se_mean": se_mean,
            "ci_mean_95": ci_mean_95,
            "ci_mean_99": ci_mean_99,
            "ci_var_95": ci_var_95,
            "degrees_of_freedom": df_freedom,
            "student_t_df": round(t_df, 2)
        },
        
        "sorted_returns_pct": [round(float(r * 100), 4) for r in sorted_ret],
        
        "histogram": {
            "counts": [round(float(c), 4) for c in counts],
            "bin_centers": [round(float(b), 3) for b in bin_centers],
            "norm_pdf": [round(float(p), 4) for p in norm_pdf],
            "t_pdf": [round(float(p), 4) for p in t_pdf],
            "laplace_pdf": [round(float(p), 4) for p in laplace_pdf],
            "logistic_pdf": [round(float(p), 4) for p in logistic_pdf]
        },
        
        "qq_plot": {
            "theoretical": [round(float(x), 3) for x in qq_theoretical],
            "sample": [round(float(y * 100), 3) for y in qq_sample]
        },
        
        "cdf": {
            "x": [round(float(x), 3) for x in cdf_x],
            "empirical": [round(float(y), 4) for y in cdf_empirical],
            "normal": [round(float(y), 4) for y in cdf_normal_vals]
        },
        
        "time_series": {
            "dates": ts_dates,
            "returns": ts_returns,
            "rolling_vol": ts_rolling_vol,
            "drawdowns": ts_drawdowns,
            "cum_wealth": ts_cum_wealth
        }
    }

# Process Core 41 Assets & Portfolios
app_database = {}

print("1. Processing primary institutional equities & benchmark...")
for ticker, meta in ASSET_METADATA.items():
    asset_df = compute_asset_series(ticker)
    merged = pd.merge(market_df[['date', 'return']], asset_df[['date', 'return']], on='date', suffixes=('_market', '_asset'))
    if len(merged) < 100:
        continue
    
    stats_data = compute_institutional_stats(
        ret_series=merged['return_asset'].values,
        dates_series=merged['date'].values,
        benchmark_returns=merged['return_market'].values
    )
    
    stats_data['meta'] = {
        'ticker': ticker,
        'name': meta['name'],
        'sector': meta['sector'],
        'category': meta['category']
    }
    
    app_database[ticker] = stats_data

# Preset Portfolios
PRESET_PORTFOLIOS = {
    'PORT_TECH': {
        'name': 'Mega-Cap Tech Alpha Portfolio',
        'sector': 'Institutional Tech Portfolio',
        'category': 'portfolio',
        'weights': {'AAPL': 0.25, 'MSFT': 0.25, 'NVDA': 0.20, 'AMZN': 0.15, 'GOOGL': 0.15}
    },
    'PORT_FINANCE': {
        'name': 'US Tier-1 Financials & Banking Portfolio',
        'sector': 'Institutional Banking Portfolio',
        'category': 'portfolio',
        'weights': {'JPM': 0.30, 'BAC': 0.25, 'GS': 0.20, 'MS': 0.15, 'WFC': 0.10}
    },
    'PORT_HEALTH': {
        'name': 'Healthcare & Biotech Defensive Portfolio',
        'sector': 'Institutional Healthcare Portfolio',
        'category': 'portfolio',
        'weights': {'JNJ': 0.30, 'UNH': 0.25, 'PFE': 0.20, 'ABBV': 0.15, 'ABT': 0.10}
    },
    'PORT_DEFENSIVE': {
        'name': 'All-Weather Inflation & Defensive Portfolio',
        'sector': 'Institutional Defensive Portfolio',
        'category': 'portfolio',
        'weights': {'JNJ': 0.20, 'PG': 0.20, 'KO': 0.20, 'WMT': 0.20, 'XOM': 0.20}
    },
    'PORT_BALANCED': {
        'name': 'Global Multi-Asset Endowment Portfolio',
        'sector': 'Institutional Balanced Portfolio',
        'category': 'portfolio',
        'weights': {'AAPL': 0.20, 'MSFT': 0.15, 'JPM': 0.15, 'JNJ': 0.15, 'XOM': 0.15, 'PG': 0.10, 'WMT': 0.10}
    }
}

print("2. Computing preset institutional portfolios...")
for port_id, p_info in PRESET_PORTFOLIOS.items():
    port_weights = p_info['weights']
    combined_dates = market_df['date'].values
    weighted_returns = np.zeros(len(combined_dates))
    
    for t_sym, w in port_weights.items():
        sub_df = compute_asset_series(t_sym)
        merged = pd.merge(market_df[['date']], sub_df[['date', 'return']], on='date', how='left').fillna(0.0)
        weighted_returns += w * merged['return'].values
    
    p_stats = compute_institutional_stats(
        ret_series=weighted_returns,
        dates_series=combined_dates,
        benchmark_returns=market_returns
    )
    
    p_stats['meta'] = {
        'ticker': port_id,
        'name': p_info['name'],
        'sector': p_info['sector'],
        'category': p_info['category'],
        'weights': port_weights
    }
    
    app_database[port_id] = p_stats

# 3. Universal S&P 500 Fast-Lookup Catalog for all 505 Tickers
print("3. Building Universal Fast-Lookup Catalog for all 505 S&P 500 Equities...")
all_tickers = sorted(df_clean['Name'].unique().tolist())
catalog_505 = []

for t in all_tickers:
    t_rets = df_clean[df_clean['Name'] == t]['daily_return'].values
    if len(t_rets) < 50:
        continue
    m = float(np.mean(t_rets))
    s = float(np.std(t_rets, ddof=1))
    sk = float(stats.skew(t_rets))
    kt = float(stats.kurtosis(t_rets))
    v99 = float(np.percentile(t_rets * 100, 1))
    cv99 = float(np.mean((t_rets * 100)[t_rets * 100 <= v99]))
    sh = float(((m * 252) - 0.045) / (s * np.sqrt(252))) if s > 0 else 0.0
    
    meta_entry = ASSET_METADATA.get(t, {'name': f'{t} Equity', 'sector': 'S&P 500 Equity'})
    
    catalog_505.append({
        "ticker": t,
        "name": meta_entry['name'],
        "sector": meta_entry['sector'],
        "mean_pct": round(m * 100, 3),
        "ann_vol_pct": round(s * np.sqrt(252) * 100, 2),
        "skewness": round(sk, 3),
        "kurtosis": round(kt, 3),
        "var_99": round(v99, 2),
        "cvar_99": round(cv99, 2),
        "sharpe": round(sh, 2)
    })

# Save Database
with open("app_data.json", "w", encoding="utf-8") as f:
    json.dump(app_database, f, indent=2)

with open("app_data.js", "w", encoding="utf-8") as f:
    f.write("window.APP_DATA = ")
    json.dump(app_database, f, indent=2)
    f.write(";\n")
    f.write("window.CATALOG_505 = ")
    json.dump(catalog_505, f, indent=2)
    f.write(";\n")

print(f"Universal pipeline finished successfully with {len(app_database)} detailed assets & {len(catalog_505)} S&P 500 catalog items!")
