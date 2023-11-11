house = read.csv("http://vsokolov.org/courses/data/stats/SaratogaHouses.csv")
head(house)
house$price =house$price/1000
plot(house$livingArea,house$price, pch=16, cex=0.5)

model=lm(price~livingArea,data=house)
coef(model)
abline(model, col="red", lwd=3)

x = 2200
13.4393940  + 0.1131225 *x

predict.lm(model, data.frame(livingArea=c(2200)))
predict.lm(model, data.frame(livingArea=c(2200)), interval = "confidence")
predict.lm(model, data.frame(livingArea=c(2200)), interval = "prediction")
predict.lm(model, data.frame(livingArea=c(3500)), interval = "prediction")

predict.lm(model, data.frame(livingArea=c(2200,3000,3500)), interval = "confidence")
predict.lm(model, data.frame(livingArea=c(2200,3000,3500)), interval = "prediction")




n = nrow(house)

s1 = sample(1:n,n/10)
s2 = sample(1:n,n/10)
plot(price~livingArea,data=house[](s1,))
lines(price~livingArea,data=house[col="red"](s2,), type="p",)
model1=lm(price~livingArea,data=house[](s1,))
model2=lm(price~livingArea,data=house[](s2,))
model1
model2
