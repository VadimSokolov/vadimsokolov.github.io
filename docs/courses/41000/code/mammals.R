setwd("~/d/slides_2019/41000/")
source("./examples/utils.R")

mammals = read.csv("data/mammals.csv")
attach(mammals)
head(mammals)
tail(mammals)

### Linear model
model = lm(Brain~Body)
# cex.lab=1.5, cex.axis=1.5, cex.main=1.5, cex.sub=1.5
layout(matrix(1:2, ncol = 2))
par(cex.lab=1.5, cex.axis=1.5, cex.main=1.5, cex.sub=1.5, pch=21, bg="white", mar=c(4.5,4.5,3,3))
plot(Body,Brain, pch=21, bg="lightblue", cex=2)
abline(model, col="red", lwd=3)
# utils$save_pdf("fig/", "mammals-model")
plot(Brain,residuals(model), bg="lightblue", pch=21, cex=2)
# utils$save_pdf("fig/", "mammals-model-res")

par(mar=c(4,4.5,3,3))
layout(matrix(1:4, ncol = 2))
plot(model, bg="lightblue", pch=21, cex=2)
# utils$save_pdf("fig/", "mammals-model-diag")


### Log-Log linear model
model = lm(log(Brain)~log(Body))
summary(model)
par(mar=c(4.5,4.5,3,3))
layout(matrix(1:2, ncol = 2))
plot(log(Brain)~log(Body), pch=21, bg="lightblue", cex=2)
abline(model, col="red", lwd=3)
plot(log(Brain),residuals(model), bg="lightblue", pch=21, cex=2)
# utils$save_pdf("fig/", "mammals-model-log")

par(mar=c(4,4.5,3,3))
layout(matrix(1:4, ncol = 2))
plot(model, bg="lightblue", pch=21, cex=2)
# utils$save_pdf("fig/", "mammals-model-log-diag")


res = rstudent(model)
outliers = order(res,decreasing = T)[](1:10)
cbind(mammals[](outliers,),
      residual = res[](outliers), 
      Fit = exp(model$fitted.values[](outliers)))