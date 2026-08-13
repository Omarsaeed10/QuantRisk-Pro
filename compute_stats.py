import pandas as pd
import numpy as np
import scipy.stats as stats

# Load data
df = pd.read_csv("data/all_stocks_5yr.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['Name', 'date'])

# Calculate daily return per stock
df['daily_return'] = df.groupby('Name')['close'].pct_change()
df_clean = df.dropna(subset=['daily_return']).copy()

# Market average daily return
market_returns = df_clean.groupby('date')['daily_return'].mean().values

n = len(market_returns)
mean = np.mean(market_returns)
var = np.var(market_returns, ddof=1)
std = np.std(market_returns, ddof=1)
skew = stats.skew(market_returns)
kurt = stats.kurtosis(market_returns) # excess kurtosis
min_ret = np.min(market_returns)
max_ret = np.max(market_returns)
median_ret = np.median(market_returns)
q25, q75 = np.percentile(market_returns, [25, 75])
iqr = q75 - q25

jb_stat, jb_p = stats.jarque_bera(market_returns)
sw_stat, sw_p = stats.shapiro(market_returns[:5000])

print("==================================================")
print("S&P 500 DAILY RETURNS STATISTICAL ANALYSIS RESULTS")
print("==================================================")
print(f"Sample Size (N): {n:,}")
print(f"Mean (mu): {mean:.6f} ({mean*100:.4f}%)")
print(f"Variance (sigma^2): {var:.8f}")
print(f"Standard Deviation (sigma): {std:.6f} ({std*100:.4f}%)")
print(f"Skewness (gamma_1): {skew:.4f}")
print(f"Excess Kurtosis (gamma_2): {kurt:.4f}")
print(f"Min Return: {min_ret:.6f} ({min_ret*100:.2f}%)")
print(f"Max Return: {max_ret:.6f} ({max_ret*100:.2f}%)")
print(f"Median Return: {median_ret:.6f} ({median_ret*100:.4f}%)")
print(f"IQR: {iqr:.6f} ({iqr*100:.4f}%)")
print(f"Jarque-Bera Stat: {jb_stat:.4f}, p-val: {jb_p:.4e}")
print(f"Shapiro-Wilk Stat: {sw_stat:.4f}, p-val: {sw_p:.4e}")
print("==================================================")

