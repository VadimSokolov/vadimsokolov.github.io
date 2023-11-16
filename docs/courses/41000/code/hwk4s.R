##  Business Statistics: Hwk4
##---------------------------------

# set your working directory
# setwd("~/....") 

#------------------------------
#   Boston House Prices
#------------------------------

require(MASS)
data("Boston")
attach(Boston)

# Data summary

help(Boston)
head(Boston)
tail(Boston)
summary(Boston)
cor(Boston)

# Scatter plots

plot(Boston)

# Density estimates, Histogram and QQ plot

# par(mfrow=c(1,3))
plot(density(medv),main='Density of Median Housing Values', 
     xlab='med. housing value', ylab='density')

hist(medv,col = "blue",main='Histogram of Median Housing Values',xlab='med. housing value')
# hist(log(medv),col = "red",main='Histogram of Log Median Housing Values',xlab='med. housing value')

qqnorm(medv,main='Normal Q-Q Plot of Median Housing Values',xlab='med. housing value')
qqline(medv)

# Multiple regression

bost = lm(medv ~ crim + indus + rm + age + dis + rad + tax + lstat, Boston)

# Extract coefficients and model summary

coef(bost)
summary(bost)

# Extract fitted value for each case

fitted(bost)

# 4-in-1 residual diagnostics

layout(matrix(c(1,2,3,4),2,2))   
plot(bost,pch=20)

detach(Boston)

#------------------------------
#   Malaria
#------------------------------

install.packages("ISwR")
library(ISwR)
data("malaria")
attach(malaria)

# Drop the irrelevant variable: subject

malaria = malaria[](,-1)

# Data summary

help(malaria)
head(malaria)
tail(malaria)
summary(malaria)
cor(malaria)

# Scatter plots

plot(malaria)

# Logistic regression

mala = glm(mal ~ age+ab,binomial)
# mala2 = glm(mal ~ age+log(ab),binomial)

# Extract coefficients and model summary

coef(mala)
summary(mala)

# Extract fitted probability/log-odds of malaria for each case

predict(mala,type = "response") # probability
predict(mala,type = "link") # log-odds

# 4-in-1 residual diagnostics

layout(matrix(c(1,2,3,4),2,2))   
plot(mala,pch=20)

# Prediction for a child of age 10 and ab = 5 level

newdata = data.frame(10,5)
colnames(newdata) = c("age","ab")
predict(mala,newdata,type = "link")
predict(mala,newdata,type = "response")
# a = sum(coef(mala)*c(1,10,5)) # log-odds
# b = 1/(1+exp(-a)) # probability

detach(malaria)

#------------------------------
#   Zagat's
#------------------------------

zagat = read.csv("http://vsokolov.org/courses/41000/data/zagat.csv",header = TRUE)
attach(zagat)

# Data summary

summary(zagat)
cor(zagat)

# Plot price versus each of the quality variables
#setEPS()
#postscript("zagat.eps",width=7,height=3)
par(mfrow=c(1,3))
plot(price~food,main="Price versus Food",pch=20,col=20,bty='n')
plot(price~decor,main="Price versus Decor",pch=20,col=20,bty='n')
plot(price~service,main="Price versus Service",pch=20,col=20,bty='n')
#dev.off()
# Multiple regression

zaga = lm(price ~ food + decor + service, zagat)

# Extract coefficients and model summary

coef(zaga)
summary(zaga)

# Extract fitted value for each case

fitted(zaga)

# 4-in-1 residual diagnostics

layout(matrix(c(1,2,3,4),2,2))   
plot(zaga,pch=20)

# Prediction for the case (food = 27, service = 25, decor = 20)

newdata = data.frame(27,25,20)
colnames(newdata) = c("food","service","decor")
predict(zaga,newdata)
# sum(coef(zaga)*c(1,27,20,25))

# Plug-in prediction interval (95%)

# Residual standard error 

se = summary(zaga)$sigma

# Upper bound
sum(coef(zaga)*c(1,27,20,25))+qnorm(0.975)*se

# Lower bound
sum(coef(zaga)*c(1,27,20,25))-qnorm(0.975)*se

detach(zagat)






#------------------------------
#   Homeless
#------------------------------

homeless = read.csv('http://vsokolov.org/courses/41000/data/homeless.csv')

model = lm(homeless.per.1000~poverty+vacancy.rate + unemployment+ public.housing + population + ave.temp + I(ave.temp.jan>60) + I(precip>800)+rent.control,data=homeless)

summary(model)
