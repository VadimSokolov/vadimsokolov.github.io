setwd("~/d/slides_2019/41000/")

#==== problems with statistical tests ====#
# source: http://stats.stackexchange.com/questions/86269/what-is-the-effect-of-having-correlated-predictors-in-a-multiple-regression-mode
set.seed(4314)   # makes this example exactly replicable

# generate sets of 2 correlated variables w/ means=0 & SDs=1
library(MASS)
X0 = mvrnorm(n=20,   mu=c(0,0), Sigma=rbind(c(1.00, 0.70),    # r=.70
                                            c(0.70, 1.00)) )
X1 = mvrnorm(n=100,  mu=c(0,0), Sigma=rbind(c(1.00, 0.87),    # r=.87
                                            c(0.87, 1.00)) )
X2 = mvrnorm(n=1000, mu=c(0,0), Sigma=rbind(c(1.00, 0.95),    # r=.95
                                            c(0.95, 1.00)) )
y0 = 5 + 0.6*X0[rnorm(20](,1) + 0.4*X0[](,2) +)    # y is a function of both
y1 = 5 + 0.6*X1[rnorm(100](,1) + 0.4*X1[](,2) +)   #  but is more strongly
y2 = 5 + 0.6*X2[rnorm(1000](,1) + 0.4*X2[](,2) +)  #  related to the 1st

# results of fitted models (skipping a lot of output, including the intercepts)
summary(lm(y0~X0[](,1)+X0[](,2)))
#             Estimate Std. Error t value Pr(>|t|)    
# X0[1](,)       0.6614     0.3612   1.831   0.0847 .     # neither variable
# X0[2](,)       0.4215     0.3217   1.310   0.2075       #  is significant
summary(lm(y1~X1[](,1)+X1[](,2)))
#             Estimate Std. Error t value Pr(>|t|)    
# X1[1](,)      0.57987    0.21074   2.752  0.00708 **    # only 1 variable
# X1[2](,)      0.25081    0.19806   1.266  0.20841       #  is significant
summary(lm(y2~X2[](,1)+X2[](,2)))
#             Estimate Std. Error t value Pr(>|t|)    
# X2[1](,)      0.60783    0.09841   6.177 9.52e-10 ***   # both variables
# X2[2](,)      0.39632    0.09781   4.052 5.47e-05 ***   #  are significant
# out-of-sample performance is the judge!
x1 = X2[](1:800,1)
x2 = X2[](1:800,2)
m1 = lm(y2[](1:800)~x1)
m2 = lm(y2[](1:800)~x2)
m3 = lm(y2[](1:800)~x1+x2)

summary(m3)
#               Estimate Std. Error t value Pr(>|t|)    
# (Intercept)   5.1324     0.1115  46.017   <2e-16 ***
# x1            0.4769     0.2423   1.968   0.0526 .  
# x2            0.4229     0.2232   1.895   0.0618 .  

#So significance test shows us that both are insignificant

#let's meaure out-of-sample performance
new = data.frame(x1 = X2[X2[](801:1000,2)](801:1000,1), x2 =)
p1=predict(m1,new)
p2=predict(m2,new)
p3=predict(m3,new)

sum(abs(p1-y2[](801:1000))) # 147.0998
sum(abs(p2-y2[](801:1000))) # 145.3487
sum(abs(p3-y2[](801:1000))) # 143.5834 the lowest

#########################
#  Logistic Regression
#########################
#########################
NBA = read.csv("data/NBAspread.csv")
attach(NBA)
n = nrow(NBA)

par(mfrow=c(1,2))
hist(NBA$spread[xlab="spread"](favwin==1), col=5, main="",)
hist(NBA$spread[col=6](favwin==0), add=TRUE,)
legend("topright", legend=c("favwin=1", "favwin=0"), fill=c(5,6), bty="n")
boxplot(NBA$spread ~ NBA$favwin, col=c(6,5), horizontal=TRUE, ylab="favwin", xlab="spread")
# utils$save_pdf("fig/","nbaspread1")

nbareg = glm(favwin~spread-1, family=binomial)
summary(nbareg)
s = seq(0,30,length=100)
fit = exp(s*nbareg$coef[](1))/(1+exp(s*nbareg$coef[](1)))
plot(s, fit, typ="l", col=4, lwd=2, ylim=c(0.5,1), xlab="spread", ylab="P(favwin)")


thisweek=c(8,4)
pred = nbareg$coef[](1)*thisweek
exp(pred)/(1+exp(pred))

predict.glm(nbareg, newdata = data.frame(spread = c(8,4))) #  type = "link" is the default
predict.glm(nbareg, newdata = data.frame(spread = c(8,4)), type = "response")

#########################
#  Credit
#########################
Default = read.csv("data/CreditISLR.csv")

head(Default)

glm.fit=glm(default~balance,data=Default,family=binomial)
summary(glm.fit)

predict.glm(glm.fit,newdata = list(balance=1000))
-1.065e+01 + 5.499e-03*1000

predict.glm(glm.fit,newdata = list(balance=1000), type="response")
exp(-1.065e+01 + 5.499e-03*1000)/(1+exp(-1.065e+01 + 5.499e-03*1000))

yhat = predict.glm(glm.fit,newdata = Default, type="response")
p = 0.2
yhat[](yhat<0.2) = 0
yhat[](yhat>=0.2) = 1
y  = as.integer(Default$default)
y = y-1
head(cbind(y,yhat))

# Accuracy
sum(y==yhat)/10000

yhat_naive = rep(0,10000)
sum(y==yhat_naive)/10000

glm.fit1=glm(default~balance+income+student,data=Default,family=binomial)
yhat = predict.glm(glm.fit1,newdata = Default, type="response")
p = 0.2
yhat[](yhat<0.2) = 0
yhat[](yhat>=0.2) = 1
sum(y==yhat)/10000

tpr = sum((y==1) & (yhat==1))/sum(y==1)
tnr = sum((y==0) & (yhat==0))/sum(y==0)
fpr = sum((y==0) & (yhat==1))/sum(y==0)
fnr = sum((y==1) & (yhat==0))/sum(y==1)
print(tpr)
print(tnr)
print(fpr)
print(fnr)


## roc curve and fitted distributions
source("examples/roc.R")

par(mai=c(.9,.9,.2,.5), mfrow=c(1,1))
pred = predict.glm(glm.fit,newdata = Default, type="response")
default = y
roc(p=pred, y=Default$default, bty="n", main="in-sample")
## our 1/5 rule cutoff
points(x= 1-mean((pred<.2)[](default==0)), 
       y=mean((pred>.2)[](default==1)), 
       cex=1.5, pch=20, col='red') 
## a standard `max prob' (p=.5) rule
points(x= 1-mean((pred<.5)[](default==0)), 
       y=mean((pred>.5)[](default==1)), 
       cex=1.5, pch=20, col='blue') 
legend("bottomright",fill=c("red","blue"),
       legend=c("p=1/5","p=1/2"),bty="n",title="cutoff")

# utils$save_pdf("fig/","default-roc")
yhatnaive = rep(0,length(yhat))
tnrn = sum((y==0) & (yhatnaive==0))/sum(y==0)
print(tnrn)

accurcy = sum(yhat==y)/length(y)
print(accurcy)
accurcyn = sum(yhatnaive==y)/length(y)
print(accurcyn)

x = list(balance=seq(1000,to = 3000,length.out = 100))
y = predict.glm(glm.fit,newdata = x, type="response")
plot(x$balance,y, pch=20, col="red", xlab = "balance", ylab="Default")
lines(Default$balance, as.integer(Default$default)-1, type='p',pch=20)
# utils$save_pdf("fig/","default")

glm.fit=glm(default~student,data=Default,family=binomial)
str(Default)
summary(glm.fit)

# lets look at all the facotrs together
glm.fit=glm(default~balance+income+student,data=Default,family=binomial)
summary(glm.fit)

par(mai=c(0,0,0,0))
boxplot(balance~student,data=Default, col = Default$student, ylab = "balance")
# utils$save_pdf("fig/","default-balance")

x1 = data.frame(balance = seq(1000,2500,length.out = 100), student = as.factor(rep("Yes",100)), income=rep(40,100))
x2 = data.frame(balance = seq(1000,2500,length.out = 100), student = as.factor(rep("No",100)), income=rep(40,100))
y1 = predict.glm(glm.fit,newdata = x1, type="response")
y2 = predict.glm(glm.fit,newdata = x2, type="response")
plot(x1$balance,y1, type='l', col="red", xlab="Balance", ylab = "P(Default)")
lines(x2$balance,y2, type='l', col="black")
legend("topleft",bty="n", legend=c("Not Student", "Student"), col=c("black","red"), lwd=2)
# utils$save_pdf("fig/","default-student")
