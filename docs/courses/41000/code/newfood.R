setwd("~/book/41000/")

newfood = read.csv("data/newfood.csv")

names(newfood)

head(newfood)
tail(newfood)

attach(newfood)
# correlation matrix
cor(cbind(sales,price,adv,locat,income,svol))


# EDA
par(mfrow=c(2,1), mar=c(4,4,1,0))
plot(newfood$price,newfood$sales, pch=16)
plot(log(newfood$price),log(newfood$sales), pch=16)

plot(newfood$income, log(newfood$sales),pch=16)
plot(log(newfood$income),log(newfood$sales), pch=16)

plot(log(newfood$sales),newfood$svol, pch=16)
plot(log(newfood$sales),log(newfood$svol), pch=16)


# Build model 
model = lm(sales~price+adv+locat, data = newfood)
mean(abs(model$fitted.values - sales)/abs(sales))
model = lm(sales~price, data=newfood)
mean(abs(model$fitted.values - sales)/abs(sales))
summary(model)

new = data.frame(price=5)
predict.lm(model,new,interval="prediction")
predict.lm(model,new,interval="confidence")



# Define a vector for prediction
new1 = data.frame(price=c(4,5,6))
predict.lm(model,new1,interval="prediction")
predict.lm(model,new1,interval="confidence")


layout(matrix(c(1,2,3,4),2,2))
plot(model)

# Transformation
# log-log model

# Can't transform dummy variables: adv, local 

log_sales = log(sales)
log_price = log(price)
log_income = log(income)
log_svol = log(svol)


# correlation matrix
cor(cbind(log_sales,log_price,adv,log_income,log_svol))

# Build model

modelnew = lm(log(sales)~log(price)+adv+log(income)+log(svol))
summary(modelnew)

# Graphics: 2x2 plot
#layout(matrix(c(1,2,3,4),2,2))


# Diagnostics

plot(modelnew)

# Prediction interval 
newdata1 = data.frame(price=30,adv=1,income=8,svol=34)
predict.lm(modelnew,newdata1,se.fit=T,interval="prediction",level=0.95)

# Conf interval
predict.lm(modelnew,newdata1,se.fit=T,interval="confidence",level=0.95)


newdata2 = data.frame(log_price=median(log_price),adv=1,
                     log_income=median(log_income),log_svol=median(log_svol))

modelnew1 = lm(log_sales~log_price+adv+log_income+log_svol)

predict.lm(modelnew1,newdata2,se.fit=T,interval="prediction")

# prediction line for log-log
layout(matrix(c(1,2,3,4),2,2))
termplot(modelnew1,ylabs="log_sales",terms="log_price",se=T)  
termplot(modelnew1,ylabs="log_sales",terms="adv",se=T)  
termplot(modelnew1,ylabs="log_sales",terms="log_income",se=T)  
termplot(modelnew1,ylabs="log_sales",terms="log_svol",se=T)  


############################################

