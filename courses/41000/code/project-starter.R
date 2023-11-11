#--------------------------------
#  Bordeaux Wine Data
#--------------------------------


mydata1 = read.table("http://vsokolov.org/courses/41000/data/bordeaux.txt",header=T)
mydata2 = read.table("http://vsokolov.org/courses/41000/data/bordeauxp.txt",header=T)

# summary statistics
summary(mydata1)

# a simple multiple regression trial
model = lm(log(price)~log(sum)+log(har)+log(sep)+log(win)+log(age),data=mydata1)

# log-log regression results
summary(model)

# residual diagnostics
par(mfrow = c(2,2), ask=F)
plot(model)


####################################################
# linear regression
# inputs: regression model and independent variables
pred = predict(model,mydata2,interval="prediction")
pred

# out-of-sample prediction line
plot(mydata2[](,1),pred[](,1),type="l",xlab="year",ylab="log_price",ylim=c(0,8),
col=2, lty=2, lwd=2,main="out-of-sample prediction line")
lines(mydata2[lwd=3](,1),pred[](,2),col=3, lty=3,)
lines(mydata2[lwd=4](,1),pred[](,3),col=4, lty=4,)
legend("topleft", c("fit","lwr","upr"),col=2:4, lty=2:4, lwd=2:4, bty="n")

# exponentiate back the predicited price
price_hat = exp(pred[](,1))
plot(mydata2[price",ylim=c(0,50](,1),price_hat,type="l",xlab="year",ylab="predicted),
col=2, lty=2, lwd=2,main="out-of-sample prediction line")

# predict new observation, for year 2017
newdata = data.frame(win = 521.07, sum = 19, sep = 19, har = 86.2, age = 3 )
exp(predict(model, newdata))

# predict new observation, for year 2018
newdata = data.frame(win = 593, sum = 20, sep = 22, har = 84.9, age = 2)
exp(predict(model, newdata))

# predict new observation, for year 2019
newdata = data.frame(win = 550, sum = 21, sep = 19, har = 110, age = 1)
exp(predict(model, newdata))