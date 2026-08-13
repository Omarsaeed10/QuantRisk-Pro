import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for modern high-quality plots
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI, DejaVu Sans, Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 1.0

def run_analysis():
    print("=" * 60)
    print("MAT231 Project: S&P 500 Daily Returns Distribution Analysis")
    print("=" * 60)
    
    # Create output directories
    os.makedirs("plots", exist_ok=True)
    
    # 1. Load Data
    csv_path = os.path.join("data", "all_stocks_5yr.csv")
    print(f"Loading data from: {csv_path}...")
    df = pd.read_csv(csv_path)
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['Name', 'date'])
    
    # Calculate daily percentage returns for each stock: (Close_t - Close_{t-1}) / Close_{t-1}
    df['daily_return'] = df.groupby('Name')['close'].pct_change()
    
    # Clean data (drop NaNs from pct_change)
    df_clean = df.dropna(subset=['daily_return']).copy()
    
    # 2. Compute Market-Wide Daily Average Return (Equal-weighted S&P 500 Index proxy)
    market_returns = df_clean.groupby('date')['daily_return'].mean().reset_index()
    market_returns.columns = ['date', 'market_return']
    
    returns = market_returns['market_return'].values
    
    # 3. Calculate Key Statistical Moments & Metrics
    n = len(returns)
    mean_val = np.mean(returns)
    var_val = np.var(returns, ddof=1)
    std_val = np.std(returns, ddof=1)
    skew_val = stats.skew(returns)
    kurt_val = stats.kurtosis(returns) # excess kurtosis (Normal = 0)
    min_val = np.min(returns)
    max_val = np.max(returns)
    median_val = np.median(returns)
    q25, q75 = np.percentile(returns, [25, 75])
    iqr_val = q75 - q25
    
    # Statistical Normality Tests
    jb_stat, jb_pvalue = stats.jarque_bera(returns)
    shapiro_stat, shapiro_pvalue = stats.shapiro(returns[:5000]) if len(returns) > 5000 else stats.shapiro(returns)
    
    print("\n--- STATISTICAL SUMMARY (S&P 500 Daily Returns) ---")
    print(f"Sample Size (n)       : {n:,} trading days")
    print(f"Mean (mu)             : {mean_val:.6f} ({mean_val*100:.4f}%)")
    print(f"Variance (sigma^2)    : {var_val:.8f}")
    print(f"Std Deviation (sigma) : {std_val:.6f} ({std_val*100:.4f}%)")
    print(f"Skewness              : {skew_val:.4f} ({'Left-skewed (negative)' if skew_val < 0 else 'Right-skewed (positive)'})")
    print(f"Excess Kurtosis       : {kurt_val:.4f} ({'Heavy-tailed / Leptokurtic' if kurt_val > 0 else 'Platykurtic'})")
    print(f"Min / Max Daily Return: {min_val*100:.2f}% / {max_val*100:.2f}%")
    print(f"Median Daily Return   : {median_val*100:.4f}%")
    print(f"IQR (Interquartile)   : {iqr_val*100:.4f}%")
    print(f"Jarque-Bera Test Stat : {jb_stat:.2f} (p-value: {jb_pvalue:.4e})")
    print(f"Shapiro-Wilk Test Stat: {shapiro_stat:.4f} (p-value: {shapiro_pvalue:.4e})")

    
    # Write summary stats to file
    with open("summary_metrics.txt", "w", encoding="utf-8") as f:
        f.write("====================================================\n")
        f.write("MAT231 PROJECT SUMMARY: S&P 500 DAILY RETURNS\n")
        f.write("====================================================\n\n")
        f.write(f"Sample Size (N): {n:,} trading days\n")
        f.write(f"Mean (μ): {mean_val:.6f} ({mean_val*100:.4f}%)\n")
        f.write(f"Variance (σ²): {var_val:.8f}\n")
        f.write(f"Standard Deviation (σ): {std_val:.6f} ({std_val*100:.4f}%)\n")
        f.write(f"Skewness: {skew_val:.4f}\n")
        f.write(f"Excess Kurtosis: {kurt_val:.4f}\n")
        f.write(f"Minimum Return: {min_val:.6f} ({min_val*100:.2f}%)\n")
        f.write(f"Maximum Return: {max_val:.6f} ({max_val*100:.2f}%)\n")
        f.write(f"Median Return: {median_val:.6f} ({median_val*100:.4f}%)\n")
        f.write(f"IQR: {iqr_val:.6f}\n")
        f.write(f"Jarque-Bera Stat: {jb_stat:.4f} (p-val: {jb_pvalue:.4e})\n")
        f.write(f"Shapiro-Wilk Stat: {shapiro_stat:.4f} (p-val: {shapiro_pvalue:.4e})\n")
    print("\nSaved summary_metrics.txt successfully.")

    # 4. Generate Visualizations
    PRIMARY_COLOR = "#1f77b4"
    NORMAL_COLOR = "#d62728"
    KDE_COLOR = "#2ca02c"
    
    # --- Plot 1: Histogram & PDF vs Fitted Normal Distribution ---
    plt.figure(figsize=(10, 6), dpi=300)
    counts, bins, patches = plt.hist(returns * 100, bins=80, density=True, alpha=0.6, color=PRIMARY_COLOR, edgecolor='white', label='Empirical Returns Histogram')
    
    # Fitted Normal Curve
    x_range = np.linspace(min(returns * 100), max(returns * 100), 1000)
    norm_pdf = stats.norm.pdf(x_range, loc=mean_val * 100, scale=std_val * 100)
    plt.plot(x_range, norm_pdf, color=NORMAL_COLOR, linewidth=2.5, linestyle='--', label=f'Fitted Normal N({mean_val*100:.2f}%, {std_val*100:.2f}%)')
    
    # KDE Curve
    sns.kdeplot(returns * 100, color=KDE_COLOR, linewidth=2, label='Kernel Density Estimate (KDE)')
    
    plt.axvline(mean_val * 100, color='darkblue', linestyle='-', linewidth=1.5, label=f'Mean (μ = {mean_val*100:.3f}%)')
    
    plt.title('Distribution of S&P 500 Daily Returns (Continuous Random Variable X)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Daily Return (%)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "01_histogram_density.png"))
    plt.close()
    print("Generated plots/01_histogram_density.png")
    
    # --- Plot 2: Q-Q Plot (Quantile-Quantile) ---
    plt.figure(figsize=(8, 6), dpi=300)
    stats.probplot(returns, dist="norm", plot=plt)
    plt.title('Q-Q Plot: Empirical Daily Returns vs Normal Distribution', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Theoretical Quantiles (Standard Normal)', fontsize=12)
    plt.ylabel('Sample Quantiles (Daily Return)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "02_qq_plot.png"))
    plt.close()
    print("Generated plots/02_qq_plot.png")

    # --- Plot 3: Time Series of Daily Returns ---
    plt.figure(figsize=(12, 5), dpi=300)
    plt.plot(market_returns['date'], market_returns['market_return'] * 100, color='#2b5c8f', linewidth=0.8, alpha=0.85)
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.axhline(mean_val * 100, color='red', linestyle=':', linewidth=1.2, label=f'Mean Return ({mean_val*100:.3f}%)')
    plt.title('S&P 500 Daily Returns Time Series', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily Return (%)', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "03_returns_time_series.png"))
    plt.close()
    print("Generated plots/03_returns_time_series.png")

    # --- Plot 4: Box Plot & Outliers ---
    plt.figure(figsize=(8, 4), dpi=300)
    sns.boxplot(x=returns * 100, color='#6baed6', fliersize=4, flierprops={'marker':'o', 'markerfacecolor':'red', 'alpha':0.5})
    plt.title('Boxplot of Daily Returns (Highlighting Fat Tails & Outliers)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Daily Return (%)', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "04_boxplot_outliers.png"))
    plt.close()
    print("Generated plots/04_boxplot_outliers.png")
    
    # --- Plot 5: Empirical CDF vs Normal CDF ---
    plt.figure(figsize=(9, 6), dpi=300)
    sorted_returns = np.sort(returns * 100)
    ecdf = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
    plt.plot(sorted_returns, ecdf, label='Empirical CDF', color='#1f77b4', linewidth=2)
    
    norm_cdf = stats.norm.cdf(sorted_returns, loc=mean_val * 100, scale=std_val * 100)
    plt.plot(sorted_returns, norm_cdf, label='Theoretical Normal CDF', color='#d62728', linestyle='--', linewidth=2)
    
    plt.title('Empirical CDF vs Theoretical Normal CDF', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Daily Return (%)', fontsize=12)
    plt.ylabel('Cumulative Probability F(x)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "05_cumulative_distribution.png"))
    plt.close()
    print("Generated plots/05_cumulative_distribution.png")

    print("\nAll analysis steps and plots completed successfully!")

if __name__ == "__main__":
    run_analysis()
