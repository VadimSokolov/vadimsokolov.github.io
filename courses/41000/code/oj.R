setwd("~/book/41000/")

oj = read.csv("./data/oj.csv")
head(oj)


model = lm(logmove ~ log(price)*feat, data=oj)
summary(model)


model = lm(log(price)~ brand-1, data = oj)
summary(model)

model = lm(log(price)~ brand, data = oj)
summary(model)


levels(oj$brand)
brandcol <- c("green","red","gold")
par(mfrow=c(1,2))
plot(log(price) ~ brand, data=oj, col=brandcol)
plot(logmove ~ log(price), data=oj, col=brandcol[oj$brand])




plot(exp(logmove) ~ price, data=oj, col=brandcol[oj$brand], pch=16, cex=0.5, ylab="move")
# utils$save_png(path = "./fig/", name = "oj")
plot(logmove ~ price, data=oj, col=brandcol[oj$brand], pch=16, cex=0.5, ylab="log(move)")
# utils$save_png(path = "./fig/", name = "oj1")
l1 <- loess(logmove ~ price, data=oj, span=2)
smoothed1 <- predict(l1) 
ind = order(oj$price)
lines(smoothed1[ind], x=oj$price[ind], col="blue", lwd=2)
# utils$save_png(path = "./fig/", name = "oj2")

plot(logmove ~ log(price), data=oj, col=brandcol[oj$brand], pch=16, cex=0.5, ylab="log(move)")
l2 <- lm(logmove ~ log(price), data=oj)
smoothed2 <- predict(l2) 
ind = order(oj$price)
lines(smoothed2[ind], x=log(oj$price[ind]), col="blue", lwd=2)
# utils$save_png(path = "./fig/", name = "oj3")


## and finally, consider 3-way interactions
ojreg <- lm(logmove ~ log(price)*feat, data=oj)
summary(ojreg)

print(lm(logmove ~ log(price), data=oj))
print(lm(logmove ~ log(price)+feat + brand, data=oj))
print(lm(logmove ~ log(price)*feat, data=oj))
print(lm(logmove ~ brand-1, data=oj))

summary(lm(logmove ~ log(price)*brand, data=oj))


library(dplyr)
doj = oj %>% filter(brand=="dominicks")

par(mfrow=c(1,3), mar=c(4.2,4.6,2,1))
boxplot(price ~  feat, data = oj[oj$brand=="dominicks",], col=c(2,3), main="dominicks", ylab="Price ($)")
boxplot(price ~  feat, data = oj[oj$brand=="minute.maid",], col=c(2,3), main="minute.maid")
boxplot(price ~  feat, data = oj[oj$brand=="tropicana",], col=c(2,3), main="tropicana")
# utils$save_pdf(path = "./fig/", name = "oj-box-all",lheight = 0.6*utils$pdf_h)

