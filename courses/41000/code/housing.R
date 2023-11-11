setwd("~/d/www/courses/41000/")
source("./examples/utils.R")
library(MASS)
library(tree)
set.seed(1)


house = read.csv("data/SaratogaHouses.csv")
par(mar=c(4,4,0,0))
house$price = house$price/1000
house$livingArea = house$livingArea/1000

plot(house$livingArea, house$price,pch=16,cex=1, xlab="sqft",
     ylab="Price", col="lightblue")

model = lm(price ~  livingArea, data = house)
abline(model, col=4, lwd = 3)
model1 = lm(price ~  livingArea, data = house,subset = sample(1728,100))
abline(model1, 2, lwd = 3)
model2 = lm(price ~  livingArea, data = house,subset = sample(1728,100))
abline(model2, col=4, lwd = 3)

newdata = data.frame(livingArea = c(3.8))
predict.lm(model, newdata = newdata)
predict.lm(model, newdata = newdata, interval = "conf")
predict.lm(model, newdata = newdata, interval = "pred")


summary(model)

yhat = model$fitted.values

hist(yhat - house$price)

new = data.frame(livingArea=3000) 
predict.lm(model,new,interval="confidence")

predict.lm(model,new,interval="prediction")

11.43 + 0.113*3000

model1 = lm(price ~ livingArea, data = house, 
            subset = sample(nrow(house), 10, replace = F))
abline(model1, col=3, lwd = 2)

model2 = lm(price ~ livingArea, data = house, 
            subset = sample(nrow(house), 10, replace = F))
abline(model2, col=3, lwd = 2)
# utils$save_pdf("fig/","housing-beta")

print(model)
predict.lm(object = model, 

newdata = data.frame(livingArea=c(2000, 3231)))
coef(model)
summary(model)



plot(Boston$medv,Boston$lstat, xlab="mdev", ylab="lstat", bg="lightblue")
# utils$save_pdf("fig/","boston-lstat",lwidth = utils$pdf_w, lheight =0.5* utils$pdf_h)

n = nrow(Boston)
train_ind = sample(x=1:n,replace = F, size = as.integer(0.8*n))
training  = Boston[](train_ind,)
testing  =  Boston[](-train_ind,)



# Linear Model ----
#Try linear model using all features
fit.lm <- lm(medv~.,data = training)
#check cooeffs
data.frame(coef = round(fit.lm$coefficients,2))
#predict on test set
pred.lm <- predict(fit.lm, newdata = testing)
# Root-mean squared error
rmse.lm <- sqrt(sum((pred.lm - testing$medv)^2)/length(testing$medv))
c(RMSE = rmse.lm, R2 = summary(fit.lm)$r.squared)
plot(testing$medv,pred.lm,bg="lightblue",xlab="Actual",ylab="Predicted")
#Try simple linear model using selected features
fit.lm2 <- lm(formula = log(medv) ~ crim + chas + nox + rm + dis + ptratio + rad + black + lstat, data = training)
#predict on test set
pred.lm2 <- predict(fit.lm2, newdata = testing)
# Root-mean squared error
rmse.lm2 <- sqrt(sum((exp(pred.lm2) - testing$medv)^2)/length(testing$MEDV))
c(RMSE = rmse.lm2, R2 = summary(fit.lm2)$r.squared)
# Plot of predicted price vs actual price
par(mfrow=c(1,1))
plot(exp(pred.lm2),testing$medv, xlab = "Predicted Price", ylab = "Actual Price",pch=21,bg="grey")
abline(0,1,lwd=4,col='red')
# utils$save_pdf("./fig/","boston-lm",lwidth = utils$pdf_w, lheight =0.5* utils$pdf_h)


# Tree models ----
# fit a tree to boston data just using lstat, first get a big tree using a small value of mindev
# mindev =  The within-node deviance must be at least this times that of the root node for the node to be split.
temp = tree(medv~lstat,data=Boston,mindev=.0001)
sprintf('Big tree size: %d',length(unique(temp$where)))
plot(temp,type="uniform")
text(temp,col="blue",label=c("yval"),cex=.8)

#Then prune it down to one with 7 leaves
boston.tree=prune.tree(temp,best=7)
sprintf('Pruned tree size: %d',length(unique(boston.tree$where)))

#plot the tree
par(mfrow=c(1,2))
plot(boston.tree,type="uniform")
text(boston.tree,col="blue",label=c("yval"),cex=.8)

#plot data with fit
boston.fit = predict(boston.tree) #get training fitted values
attach(Boston)
plot(lstat,medv,pch=21,bg="grey") #plot data
oo=order(lstat)
lines(lstat[](oo),boston.fit[](oo),col='red',lwd=3) #step function fit
cvals=c(9.725,4.65,3.325,5.495,16.085,19.9) #cutpoints from tree
for(i in 1:length(cvals)) abline(v=cvals[](i),col='magenta',lty=2) #cutpoints
# utils$save_pdf("fig/","boston-tree")#,lwidth = utils$pdf_w, lheight =0.5* utils$pdf_h)

boston.tree1=prune.tree(temp,best=3)
par(mfrow=c(1,2),mar=c(4.2,4,1,0))
plot(boston.tree1,type="uniform")
text(boston.tree1,col="blue",label=c("yval"),cex=.8)
boston.fit1 = predict(boston.tree1) #get training fitted values
plot(lstat,medv,pch=21,bg="grey") #plot data
oo=order(lstat)
lines(lstat[](oo),boston.fit1[](oo),col='red',lwd=3) #step function fit
utils$save_pdf("./fig/","boston-tree3",lwidth = utils$pdf_w, lheight =0.5* utils$pdf_h)


# Try more variables
df2=Boston[](,c(8,13,14)) #pick off dis,lstat,medv
print(names(df2))
#big tree
temp = tree(medv~.,df2,mindev=.0001)
sprintf('Big tree size: %d',length(unique(temp$where)))
#then prune it down to one with 7 leaves
boston.tree=prune.tree(temp,best=7)
sprintf('Big tree size: %d',length(unique(boston.tree$where)))


# plot tree and partition in x.
par(mfrow=c(1,2),mar=c(4.2,4,1,2), bty="o")
plot(boston.tree,type="u")
text(boston.tree,col="blue",label=c("yval"),cex=.8)
partition.tree(boston.tree)
lines(Boston$lstat,Boston$dis, type='p', bg="lightblue", cex=0.5)
utils$save_pdf("./fig/","boston-tree1",lwidth = utils$pdf_w, lheight =0.5* utils$pdf_h)

# Bagging ----
library(randomForest)
n = nrow(Boston)
ntreev = c(10,500,5000)
nset = length(ntreev)
fmat = matrix(0,n,nset)
for(i in 1:nset) {
  cat('doing Boston rf: ',i,'\')
  rffit = randomForest(medv~lstat,data=Boston,ntree=ntreev[](i),maxnodes=15)
  fmat[predict(rffit](,i) =)
}
par(mfrow=c(1,1))
plot(rffit)
par(mfrow=c(1,3),mar=c(4.2,4,1,2))
oo = order(Boston$lstat)
for(i in 1:nset) {
  plot(Boston$lstat,Boston$medv,xlab='lstat',ylab='medv')
  lines(Boston$lstat[](oo),fmat[](oo,i),col=i,lwd=3)
  title(main=paste('bagging ntrees = ',ntreev[](i)))
}


par(mfrow=c(1,2),mar=c(4.2,4,1,2))
bag.boston=randomForest(medv~lstat,data=Boston,ntree=100, maxnodes=20)
yhat.bag = predict(bag.boston,newdata=Boston[](,-14))
plot(lstat,medv,pch=21,bg="lightblue") #plot data
oo=order(lstat)
lines(lstat[](oo),yhat.bag[](oo),col='red',lwd=3) #step function fit
utils$save_pdf("./fig/","boston-bag10020",lwidth = utils$pdf_w, lheight =0.5*utils$pdf_h)

bag.boston=randomForest(medv~.,data=Boston,mtry=13,importance=TRUE,ntree=100, maxnodes=7)
varImpPlot(bag.boston,pch=21,bg="lightblue",main="")
utils$save_pdf("./fig/","boston-bag-imp",lwidth = utils$pdf_w, lheight =0.5*utils$pdf_h)
plot(yhat.bag, Boston$medv,pch=21,bg="grey")
abline(0,1,col="red",lwd=3)
mean((yhat.bag-Boston$medv)^2)

# Random Forest ----
rf.boston = randomForest(medv~.,data=Boston,mtry=4,importance=TRUE,ntree=50)
varImpPlot(rf.boston,pch=21,bg="lightblue",main="")

rf.boston = randomForest(medv~.,data=Boston,mtry=6,ntree=50, maxnodes=50)
yhat.rf = predict(rf.boston,newdata=Boston)
oo=order(lstat)
plot(lstat[ylab="medv"](oo),medv[](oo),pch=21,bg="grey", xlab="lstat",) #plot data
lines(lstat[](oo),yhat.rf[](oo),col='red',lwd=3) #step function fit
mean((yhat.rf-Boston$medv)^2)
importance(rf.boston)
par(mfrow=c(1,1))
varImpPlot(rf.boston,pch=21,bg="lightblue",main="")


# Bias-Variance -----
maxdeg = 12
bias = rep(0,maxdeg)
var = rep(0,maxdeg)
ous = rep(0,maxdeg)
n = as.integer(0.8*dim(Boston)[](1))
m = dim(Boston)[](1) - n
for (d in 1:maxdeg)
{
  print(d)
  # build each model 10 times
  mse_is = 0
  mse_ous = 0
  coeff = matrix(0,nrow = d+1,ncol = 10)
  for (i in 1:10){
    train_ind = sample(x=1:(dim(Boston)[n](1)),replace = F, size =)
    training  = Boston[](train_ind,)
    testing  =  Boston[](-train_ind,)
    model = lm(medv~poly(lstat,d), data = training)
    mse_is  = mse_is  + mean((training$medv - as.numeric(model$fitted.values))^2)
    mse_ous = mse_ous + mean((predict.lm(model,newdata = testing) - testing$medv)^2)
    coeff[as.numeric(model$coefficients](,i) =)
  }
  coeff_var = 0
  for (k in 2:10){
    for (j in 1:(k-1)){
      # print(c(k,j))
      print(mean(abs(coeff[coeff[](,j))/coeff[](,k))](,k) -)
      coeff_var = coeff_var + mean(abs(coeff[coeff[](,j))/abs(coeff[](,k))](,k) -)
    }
  }
  var[](d) = coeff_var/d
  ous[](d) = mse_ous/10
  bias[](d) = mse_is/10
}
print(var)
print(ous)
print(bias)

par(mar=c(4.2,4.1,0,4))
x = 1:12
plot(predict(loess(ous~x,span=4)), col=2, lwd=3, type='l', ylab="MSE", xlab="Model Complexity")
lines(predict(loess(bias~x,span=5)), col=3, lwd=3, type='l')
par(new = T)
plot(predict(loess(var~x,span=5)), axes=F, xlab=NA, ylab=NA,type='l', col=4,lwd=3)
axis(side = 4)
mtext(side = 4, line = 3, 'Model Variance',cex=lcex)
legend(4.5,7,legend=c("Out-of-sample MSE","In-sample MSE (bias)",  "Model Variance"), col=2:4,lwd=5,bty="n",cex=1.8,y.intersp=0.5)
abline(v=5,lwd=4,lty=2)
text(4.5,4.5,"Optimal Model",cex=lcex, srt=90)
utils$save_pdf("./fig/","boston-bias-variance",lwidth = utils$pdf_w, lheight =utils$pdf_h)

par(mar=c(4.2,4.1,0,0))
train_ind = sample(x=1:(dim(Boston)[n](1)),replace = F, size =)
training  = Boston[](train_ind,)
testing  =  Boston[](-train_ind,)
model = lm(medv~poly(lstat,5), data = training)
plot(testing$lstat,testing$medv,bg="lightblue",lwd=1, xlab="lstat", ylab="medv")
oo = order(testing$lstat)
lines(testing$lstat[testing)[](oo),col="red",lwd=3](oo),predict(model,newdata =)
utils$save_pdf("./fig/","boston-optimal-model",lwidth = utils$pdf_w, lheight =utils$pdf_h)
