import pandas as pd
import numpy as np
import scipy.stats as stats
import json

# Load dataset
df = pd.read_csv("data/all_stocks_5yr.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Name', 'date'])

# Calculate pct returns
df['daily_return'] = df.groupby('Name')['close'].pct_change()
df_clean = df.dropna(subset=['daily_return']).copy()

# Market returns
market_df = df_clean.groupby('date')['daily_return'].mean().reset_index()
market_df.columns = ['date', 'return']

def get_stats(returns):
    ret = np.array(returns)
    n = len(ret)
    mean = float(np.mean(ret))
    var = float(np.var(ret, ddof=1))
    std = float(np.std(ret, ddof=1))
    skew = float(stats.skew(ret))
    kurt = float(stats.kurtosis(ret))
    min_val = float(np.min(ret))
    max_val = float(np.max(ret))
    median = float(np.median(ret))
    q25, q75 = [float(x) for x in np.percentile(ret, [25, 75])]
    iqr = q75 - q25
    jb_stat, jb_p = [float(x) for x in stats.jarque_bera(ret)]
    
    # Standard Error & CIs
    se_mean = float(std / np.sqrt(n))
    z_critical = 1.95996
    ci_mean_lower = mean - z_critical * se_mean
    ci_mean_upper = mean + z_critical * se_mean
    
    df_freedom = n - 1
    chi2_lower = stats.chi2.ppf(0.025, df_freedom)
    chi2_upper = stats.chi2.ppf(0.975, df_freedom)
    ci_var_lower = (df_freedom * var) / chi2_upper
    ci_var_upper = (df_freedom * var) / chi2_lower
    
    # Value at Risk (VaR) Calculations (Real-world Continuous RV Application)
    # 95% & 99% Historical (Empirical Percentiles)
    var_hist_95 = float(np.percentile(ret * 100, 5))
    var_hist_99 = float(np.percentile(ret * 100, 1))
    
    # 95% & 99% Parametric Normal
    var_norm_95 = float((mean * 100) - 1.64485 * (std * 100))
    var_norm_99 = float((mean * 100) - 2.32635 * (std * 100))
    
    # Histogram bins (50 bins)
    counts, bin_edges = np.histogram(ret * 100, bins=50, density=True)
    bin_centers = [(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(counts))]
    
    # Fitted normal curve points
    norm_pdf = [float(stats.norm.pdf(x, loc=mean*100, scale=std*100)) for x in bin_centers]
    
    # Fitted Student-t curve points (heavy tail model fit)
    t_params = stats.t.fit(ret * 100)
    t_pdf = [float(stats.t.pdf(x, *t_params)) for x in bin_centers]
    
    # Q-Q plot quantiles
    res = stats.probplot(ret, dist="norm")
    step_qq = max(1, int(len(ret)/100))
    qq_theoretical = [float(x) for x in res[0][0][::step_qq]]
    qq_sample = [float(x) for x in res[0][1][::step_qq]]
    
    # CDF
    sorted_ret = np.sort(ret * 100)
    step_cdf = max(1, int(len(sorted_ret) / 100))
    cdf_x = [float(x) for x in sorted_ret[::step_cdf]]
    cdf_empirical = [float((i*step_cdf + 1) / len(sorted_ret)) for i in range(len(cdf_x))]
    cdf_normal_vals = [float(stats.norm.cdf(x, loc=mean*100, scale=std*100)) for x in cdf_x]
    
    return {
        "n": n,
        "mean": mean,
        "variance": var,
        "std": std,
        "skewness": skew,
        "kurtosis": kurt,
        "min": min_val,
        "max": max_val,
        "median": median,
        "q25": q25,
        "q75": q75,
        "iqr": iqr,
        "jb_stat": jb_stat,
        "jb_p": jb_p,
        "var_metrics": {
            "hist_95": var_hist_95,
            "hist_99": var_hist_99,
            "norm_95": var_norm_95,
            "norm_99": var_norm_99
        },
        "lecture_metrics": {
            "se_mean": se_mean,
            "ci_mean": [ci_mean_lower, ci_mean_upper],
            "ci_var": [ci_var_lower, ci_var_upper],
            "degrees_of_freedom": df_freedom
        },
        "sorted_returns_pct": [round(float(r * 100), 4) for r in sorted_ret],
        "histogram": {
            "counts": [float(c) for c in counts],
            "bin_centers": [round(b, 3) for b in bin_centers],
            "norm_pdf": [round(p, 4) for p in norm_pdf],
            "t_pdf": [round(p, 4) for p in t_pdf]
        },
        "qq_plot": {
            "theoretical": [round(x, 3) for x in qq_theoretical],
            "sample": [round(y*100, 3) for y in qq_sample]
        },
        "cdf": {
            "x": [round(x, 3) for x in cdf_x],
            "empirical": [round(y, 4) for y in cdf_empirical],
            "normal": [round(y, 4) for y in cdf_normal_vals]
        }
    }

tickers = ['MARKET_AVG', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA', 'JPM']
output_data = {}

for ticker in tickers:
    if ticker == 'MARKET_AVG':
        sub_df = market_df
        rets = sub_df['return'].values
        dates = sub_df['date'].dt.strftime('%Y-%m-%d').tolist()
    else:
        sub_df = df_clean[df_clean['Name'] == ticker]
        if len(sub_df) == 0:
            continue
        rets = sub_df['daily_return'].values
        dates = sub_df['date'].dt.strftime('%Y-%m-%d').tolist()
        
    stats_dict = get_stats(rets)
    stats_dict['time_series'] = {
        "dates": dates[::2],
        "returns": [round(float(r)*100, 3) for r in rets[::2]]
    }
    output_data[ticker] = stats_dict

with open("app_data.json", "w") as f:
    json.dump(output_data, f)

with open("app_data.js", "w") as f:
    f.write(f"window.APP_DATA = {json.dumps(output_data)};")

print("Exported app_data.json and app_data.js with VaR and Student-t fit successfully!")
