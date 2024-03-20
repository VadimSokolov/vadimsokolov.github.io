d5 = rpois(n = 1000,lambda = 5)
d2 = rpois(n = 1000,lambda = 2)
hist(d2, col = "blue",freq = F, main="", xlab="Poisson", xlim = c(0,8))
hist(d5, col = "purple", add=T, freq = F)
legend("topright", legend = c("lambda = 2", "lambda = 5"), fill = c("blue", "purple"))

d = data.frame(lambda_5=d5,lambda_2=d2)
boxplot(d,horizontal = T, col=c("blue", "purple"))

        