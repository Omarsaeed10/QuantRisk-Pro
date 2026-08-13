# ==============================================================================
# MAT231 Project: S&P 500 Daily Returns Analysis in R
# Concept: Continuous Random Variables & Probability Distributions
# ==============================================================================

# Install required packages if not already present
required_packages <- c("dplyr", "ggplot2", "moments", "qqplotr")
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

library(dplyr)
library(ggplot2)
library(moments)

cat("====================================================\n")
cat("MAT231 Project: S&P 500 Daily Returns Analysis (R)\n")
cat("====================================================\n\n")

# 1. Load Data
csv_path <- "data/all_stocks_5yr.csv"
if (!file.exists(csv_path)) {
  stop("CSV data file not found at data/all_stocks_5yr.csv!")
}

data <- read.csv(csv_path, stringsAsFactors = FALSE)
data$date <- as.Date(data$date)

# Sort data
data <- data %>% arrange(Name, date)

# 2. Compute Daily Returns for each stock
data <- data %>%
  group_by(Name) %>%
  mutate(daily_return = (close - lag(close)) / lag(close)) %>%
  filter(!is.na(daily_return))

# Market Average Return per day
market_returns <- data %>%
  group_by(date) %>%
  summarise(market_return = mean(daily_return, na.rm = TRUE))

returns <- market_returns$market_return

# 3. Compute Statistical Moments
n_obs      <- length(returns)
mean_val   <- mean(returns)
var_val    <- var(returns)
sd_val     <- sd(returns)
skew_val   <- moments::skewness(returns)
kurt_val   <- moments::kurtosis(returns) - 3  # excess kurtosis
min_val    <- min(returns)
max_val    <- max(returns)
median_val <- median(returns)
iqr_val    <- IQR(returns)

cat(sprintf("Sample Size (n)       : %d trading days\n", n_obs))
cat(sprintf("Mean (mu)             : %.6f (%.4f%%)\n", mean_val, mean_val * 100))
cat(sprintf("Variance (sigma^2)    : %.8f\n", var_val))
cat(sprintf("Std Deviation (sigma) : %.6f (%.4f%%)\n", sd_val, sd_val * 100))
cat(sprintf("Skewness              : %.4f\n", skew_val))
cat(sprintf("Excess Kurtosis       : %.4f\n", kurt_val))
cat(sprintf("Min / Max Daily Return: %.2f%% / %.2f%%\n", min_val * 100, max_val * 100))
cat(sprintf("Median Daily Return   : %.4f%%\n", median_val * 100))
cat(sprintf("IQR                   : %.4f%%\n", iqr_val * 100))

# Shapiro-Wilk Test for Normality (sample up to 5000)
sample_for_shapiro <- head(returns, 5000)
shapiro_res <- shapiro.test(sample_for_shapiro)
cat(sprintf("Shapiro-Wilk W-stat   : %.4f (p-value: %e)\n", shapiro_res$statistic, shapiro_res$p.value))

# 4. Save Plots
dir.create("plots_r", showWarnings = FALSE)

# Plot 1: Histogram + Normal Overlay
p1 <- ggplot(market_returns, aes(x = market_return * 100)) +
  geom_histogram(aes(y = ..density..), bins = 80, fill = "#1f77b4", color = "white", alpha = 0.6) +
  stat_function(fun = dnorm, args = list(mean = mean_val * 100, sd = sd_val * 100), color = "#d62728", size = 1.2, linetype = "dashed") +
  geom_density(color = "#2ca02c", size = 1) +
  labs(title = "S&P 500 Daily Returns Distribution (R)",
       x = "Daily Return (%)", y = "Density") +
  theme_minimal()

ggsave("plots_r/r_histogram.png", plot = p1, width = 8, height = 5, dpi = 300)

# Plot 2: Q-Q Plot
p2 <- ggplot(market_returns, aes(sample = market_return)) +
  stat_qq(color = "#1f77b4", alpha = 0.6) +
  stat_qq_line(color = "#d62728", size = 1) +
  labs(title = "Q-Q Plot: Normal Distribution Check (R)",
       x = "Theoretical Quantiles", y = "Sample Quantiles") +
  theme_minimal()

ggsave("plots_r/r_qqplot.png", plot = p2, width = 7, height = 5, dpi = 300)

cat("\nR Analysis & Plots finished successfully!\n")
