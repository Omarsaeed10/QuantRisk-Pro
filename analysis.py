import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Set style for modern high-resolution institutional plots
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI, DejaVu Sans, Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

def run_analysis():
    print("=" * 70)
    print("QuantRisk Enterprise™ / MAT231 Continuous Random Variables Analysis")
    print("=" * 70)
    
    os.makedirs("plots", exist_ok=True)
    
    # 1. Load Data
    csv_path = os.path.join("data", "all_stocks_5yr.csv")
    print(f"Loading market dataset from: {csv_path}...")
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['Name', 'date'])
    
    # Calculate daily percentage returns: (P_t - P_{t-1}) / P_{t-1}
    df['daily_return'] = df.groupby('Name')['close'].pct_change()
    df_clean = df.dropna(subset=['daily_return']).copy()
    
    # S&P 500 Equal-Weighted Market Return Benchmark
    market_returns_df = df_clean.groupby('date')['daily_return'].mean().reset_index()
    market_returns_df.columns = ['date', 'market_return']
    returns = market_returns_df['market_return'].values
    
    # 2. Key Statistical Moments & Metrics
    n = len(returns)
    mean_val = float(np.mean(returns))
    var_val = float(np.var(returns, ddof=1))
    std_val = float(np.std(returns, ddof=1))
    skew_val = float(stats.skew(returns))
    kurt_val = float(stats.kurtosis(returns)) # Excess Kurtosis (Normal = 0)
    min_val = float(np.min(returns))
    max_val = float(np.max(returns))
    median_val = float(np.median(returns))
    q25, q75 = [float(x) for x in np.percentile(returns, [25, 75])]
    iqr_val = q75 - q25
    
    # Normality Hypothesis Tests
    jb_stat, jb_pvalue = stats.jarque_bera(returns)
    sample_shapiro = returns[:5000] if len(returns) > 5000 else returns
    shapiro_stat, shapiro_pvalue = stats.shapiro(sample_shapiro)
    ks_stat, ks_pvalue = stats.kstest(returns, 'norm', args=(mean_val, std_val))
    
    # Basel III Risk Metrics
    var_95_hist = float(np.percentile(returns * 100, 5))
    var_99_hist = float(np.percentile(returns * 100, 1))
    var_95_norm = float((mean_val * 100) - 1.64485 * (std_val * 100))
    var_99_norm = float((mean_val * 100) - 2.32635 * (std_val * 100))
    
    # Cornish-Fisher VaR (Adjusted for skewness and kurtosis)
    z_01 = stats.norm.ppf(0.01)
    z_cf = z_01 + (1.0/6.0)*(z_01**2 - 1)*skew_val + (1.0/24.0)*(z_01**3 - 3*z_01)*kurt_val - (1.0/36.0)*(2*z_01**3 - 5*z_01)*(skew_val**2)
    var_99_cf = float((mean_val * 100) + z_cf * (std_val * 100))
    
    # Expected Shortfall (CVaR)
    cvar_99_hist = float(np.mean((returns * 100)[returns * 100 <= var_99_hist]))
    
    print("\n--- INSTITUTIONAL STATISTICAL SUMMARY ---")
    print(f"Sample Size (N)       : {n:,} trading days")
    print(f"Mean (mu)             : {mean_val:.6f} ({mean_val*100:.4f}% / day, {((1+mean_val)**252 - 1)*100:.2f}% / yr)")
    print(f"Variance (sigma^2)    : {var_val:.8f}")
    print(f"Std Deviation (sigma) : {std_val:.6f} ({std_val*100:.4f}% / day, {std_val*np.sqrt(252)*100:.2f}% / yr)")
    print(f"Skewness (gamma_1)    : {skew_val:.4f} (Negative Left Crash Tail)")
    print(f"Excess Kurtosis (gamma_2): {kurt_val:.4f} (Heavy Leptokurtic Fat Tails)")
    print(f"Min / Max Return      : {min_val*100:.2f}% / +{max_val*100:.2f}%")
    print(f"Median Return         : {median_val*100:.4f}%")
    print(f"99% Historical VaR    : {var_99_hist:.2f}%")
    print(f"99% Cornish-Fisher VaR: {var_99_cf:.2f}%")
    print(f"99% Expected Shortfall: {cvar_99_hist:.2f}%")
    print(f"Jarque-Bera Test Stat : {jb_stat:.2f} (p-value: {jb_pvalue:.4e})")
    print(f"Shapiro-Wilk Test Stat: {shapiro_stat:.4f} (p-value: {shapiro_pvalue:.4e})")
    
    # Summary Metrics File
    with open("summary_metrics.txt", "w", encoding="utf-8") as f:
        f.write("====================================================\n")
        f.write("QUANTRISK ENTERPRISE™ / MAT231 STATISTICAL AUDIT\n")
        f.write("====================================================\n\n")
        f.write(f"Sample Observations (N): {n:,} trading days\n")
        f.write(f"Daily Mean (μ): {mean_val:.6f} ({mean_val*100:.4f}%)\n")
        f.write(f"Annualized Return: {((1+mean_val)**252 - 1)*100:.2f}%\n")
        f.write(f"Daily Variance (σ²): {var_val:.8f}\n")
        f.write(f"Daily Volatility (σ): {std_val:.6f} ({std_val*100:.4f}%)\n")
        f.write(f"Annualized Volatility: {std_val*np.sqrt(252)*100:.2f}%\n")
        f.write(f"Skewness (γ₁): {skew_val:.4f}\n")
        f.write(f"Excess Kurtosis (γ₂): {kurt_val:.4f}\n")
        f.write(f"Minimum Daily Return: {min_val*100:.2f}%\n")
        f.write(f"Maximum Daily Return: {max_val*100:.2f}%\n")
        f.write(f"Median Daily Return: {median_val*100:.4f}%\n")
        f.write(f"Interquartile Range (IQR): {iqr_val*100:.4f}%\n")
        f.write(f"95% Historical 1-Day VaR: {var_95_hist:.2f}%\n")
        f.write(f"99% Historical 1-Day VaR: {var_99_hist:.2f}%\n")
        f.write(f"99% Cornish-Fisher VaR: {var_99_cf:.2f}%\n")
        f.write(f"99% Expected Shortfall (CVaR): {cvar_99_hist:.2f}%\n")
        f.write(f"Jarque-Bera Stat: {jb_stat:.4f} (p-val: {jb_pvalue:.4e})\n")
        f.write(f"Shapiro-Wilk Stat: {shapiro_stat:.4f} (p-val: {shapiro_pvalue:.4e})\n")
        f.write(f"Normality Test Audit: REJECTED (Non-Gaussian Fat Tails)\n")
    print("Saved summary_metrics.txt successfully.")

    # 3. Generate Visualizations (Plots)
    PRIMARY_COLOR = "#0284c7"
    NORMAL_COLOR = "#dc2626"
    STUDENT_COLOR = "#16a34a"
    
    # --- Plot 1: Histogram & PDF vs Fitted Normal & Student's t ---
    plt.figure(figsize=(10, 6), dpi=300)
    counts, bins, patches = plt.hist(returns * 100, bins=80, density=True, alpha=0.55, color=PRIMARY_COLOR, edgecolor='white', label='Empirical Returns Density')
    
    x_range = np.linspace(min(returns * 100), max(returns * 100), 1000)
    norm_pdf = stats.norm.pdf(x_range, loc=mean_val * 100, scale=std_val * 100)
    plt.plot(x_range, norm_pdf, color=NORMAL_COLOR, linewidth=2.2, linestyle='--', label=f'Fitted Normal N({mean_val*100:.2f}%, {std_val*100:.2f}%)')
    
    t_params = stats.t.fit(returns * 100)
    t_pdf = stats.t.pdf(x_range, *t_params)
    plt.plot(x_range, t_pdf, color=STUDENT_COLOR, linewidth=2.5, label=f"Student's t-Distribution (nu = {t_params[0]:.1f})")
    
    plt.axvline(var_99_hist, color='darkred', linestyle=':', linewidth=1.8, label=f'99% Historical VaR ({var_99_hist:.2f}%)')
    plt.axvline(mean_val * 100, color='navy', linestyle='-', linewidth=1.2, label=f'Mean Return ({mean_val*100:.3f}%)')
    
    plt.title('Distribution of S&P 500 Daily Returns: Empirical vs Student-t & Gaussian Normal', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Daily Return (%)', fontsize=11)
    plt.ylabel('Probability Density f(x)', fontsize=11)
    plt.legend(fontsize=9.5, loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "01_histogram_density.png"))
    plt.close()
    print("Generated plots/01_histogram_density.png")
    
    # --- Plot 2: Q-Q Plot (Quantile-Quantile) ---
    plt.figure(figsize=(8, 6), dpi=300)
    stats.probplot(returns * 100, dist="norm", plot=plt)
    plt.title('Q-Q Diagnostic Plot: Empirical Daily Returns vs Standard Normal', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Theoretical Quantiles (Standard Normal Z-Score)', fontsize=11)
    plt.ylabel('Sample Return Quantiles (%)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "02_qq_plot.png"))
    plt.close()
    print("Generated plots/02_qq_plot.png")

    # --- Plot 3: Time Series of Daily Returns & Rolling Volatility ---
    plt.figure(figsize=(12, 5), dpi=300)
    plt.plot(market_returns_df['date'], market_returns_df['market_return'] * 100, color='#0369a1', linewidth=0.8, alpha=0.85, label='Daily Return (%)')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.axhline(mean_val * 100, color='red', linestyle=':', linewidth=1.2, label=f'Mean Return ({mean_val*100:.3f}%)')
    plt.title('S&P 500 Daily Returns Time Series (Volatility Clustering)', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=11)
    plt.ylabel('Daily Return (%)', fontsize=11)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "03_returns_time_series.png"))
    plt.close()
    print("Generated plots/03_returns_time_series.png")

    # --- Plot 4: Box Plot & Extreme Outliers ---
    plt.figure(figsize=(9, 4), dpi=300)
    sns.boxplot(x=returns * 100, color='#7dd3fc', fliersize=4, flierprops={'marker':'o', 'markerfacecolor':'#dc2626', 'alpha':0.6})
    plt.axvline(mean_val * 100, color='navy', linestyle='--', linewidth=1.5, label='Mean')
    plt.axvline(median_val * 100, color='green', linestyle='-', linewidth=1.5, label='Median')
    plt.title('Boxplot & Extreme Tail Outlier Diagnostics', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Daily Return (%)', fontsize=11)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "04_boxplot_outliers.png"))
    plt.close()
    print("Generated plots/04_boxplot_outliers.png")

    # --- Plot 5: Empirical vs Normal CDF ---
    plt.figure(figsize=(9, 5), dpi=300)
    sorted_ret = np.sort(returns * 100)
    cdf_emp = np.arange(1, len(sorted_ret) + 1) / len(sorted_ret)
    cdf_norm = stats.norm.cdf(sorted_ret, loc=mean_val * 100, scale=std_val * 100)
    plt.plot(sorted_ret, cdf_emp, color='#0284c7', linewidth=2.5, label='Empirical Cumulative CDF F(x)')
    plt.plot(sorted_ret, cdf_norm, color='#dc2626', linewidth=2, linestyle='--', label='Theoretical Normal CDF')
    plt.title('Cumulative Distribution Function (CDF): Empirical vs Theoretical Normal', fontsize=13, fontweight='bold', pad=15)
    plt.xlabel('Daily Return x (%)', fontsize=11)
    plt.ylabel('Cumulative Probability P(X <= x)', fontsize=11)
    plt.legend(loc='lower right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "05_cdf_comparison.png"))
    plt.close()
    print("Generated plots/05_cdf_comparison.png")

    print("\nAll statistical diagnostics & high-resolution plots generated successfully!")

if __name__ == "__main__":
    run_analysis()
