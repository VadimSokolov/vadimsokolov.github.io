##  Problem 5
##  Portfolio Means, Standard Deviations and Correlations
##---------------------------------------
install.packages("quantmod")

library(quantmod)

# load data from yahoo finance
getSymbols('VUG', from = "2006-01-01")
getSymbols('VTV', from = "2006-01-01")


VUG # take a look to the data

# pick daily closing price only
VUG = VUG$VUG.Close
VTV = VTV$VTV.Close

# Plot the historical price of VUG vs VTV.
par(mfrow = c(1,2))
plot(VUG)
plot(VTV)

# compute return of two ETFs
VUG.return = dailyReturn(VUG)
VTV.return = dailyReturn(VTV)

# plot histogram of daily returns of two ETFs
par(mfrow = c(1,2))
hist(VUG.return, breaks = 50)
hist(VTV.return, breaks = 50)


# Calculate the means and standard deviations of both ETFs.
mean(VUG.return)
mean(VTV.return)
sd(VUG.return)
sd(VTV.return)

# Calculate the covariance between them.
cov(VUG.return, VTV.return)

# Suppose you decide on a 50-50 split portfolio, calculate mean and variance of your portfolio.
portfolio_return = 0.5 * VUG.return + 0.5 * VTV.return
hist(portfolio_return, breaks = 50)

# compute mean and variance of return of the portfolio
portfolio_mean_1 = 0.5 * mean(VUG.return) + 0.5 * mean(VTV.return)
portfolio_var_1 = 0.5^2 * var(VUG.return) + 0.5^2 * var(VTV.return) + 2 * 0.5 * 0.5 * cov(VUG.return, VTV.return)
portfolio_sd_1 = sqrt(portfolio_var_1)

print(portfolio_mean_1)
print(portfolio_var_1)
print(portfolio_sd_1)

# Which alternative portfolio best suits you?

# the choice of portfolio depends on your own risk preference