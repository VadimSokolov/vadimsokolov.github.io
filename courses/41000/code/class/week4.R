d = read.csv("~/www/courses/data/stats/GOOG.csv")
head(d)
n = nrow(d)

ret = (d$Adj.Close[d$Adj.Close[](1:(n-1)))/d$Adj.Close[](1:(n-1)](2:n) -)
ret = ret[](!is.na(ret))
n = length(ret)
hist(ret, breaks = 50, freq = FALSE)

mu = mean(ret)
s = sd(ret)

rdens = dnorm(ret,mu,s)
lines(ret,rdens, type='p', pch=16, cex=0.5)

# P(ret < -0.03)
pnorm(-0.01,mu,s)
sum(ret   < -0.01)/n


n = 2500

wavg = rep(0,10000)
for (i in 1:10000){
  w = rnorm(n,100,1)
  wavg[mean(w](i) =)
}


hist(wavg,breaks=30)

sd(wavg)


prop.test(c(1755,1818),c(2500,2500), alternative = "less", correct = F)


# MI elections
true_prop  = 0.56
proprtions = rep(0,10000)
for(i in 1:10000){
  survey = rbinom(1000,size = 1,prob = true_prop)
  survey_prop = sum(survey==1)/1000
  proprtions[](i) = survey_prop 
}

hist(proprtions, breaks = 50, freq = FALSE)

survey = rbinom(1000,size = 1,prob = true_prop)
phat = sum(survey==1)/1000
varphat = phat*(1-phat)
var(survey)


phat1 = 1755/2500
phat2 = 1818/2500
x = seq(0.66,0.76,by=0.001)
rdens1 = dnorm(x,phat1,sqrt(phat1*(1-phat1)/2500))
rdens2 = dnorm(x,phat2,sqrt(phat2*(1-phat2)/2500))
plot(x,rdens1, type='l', pch=16, cex=0.5, lwd = 2)
lines(x,rdens2, type='l', pch=16, cex=0.5, col="red", lwd=2)


# Pepsi
x = seq(0.4,0.6,by=0.001)
p = 0.5
phat = 0.56
rdens1 = dnorm(x,p,sqrt(phat*(1-phat)/2500))

plot(x,rdens1, type='l', pch=16, cex=0.5, lwd = 2)
lines(x,rdens2, type='l', pch=16, cex=0.5, col="red", lwd=2)


1 - pnorm(0.56,0.5, sqrt(0.56*(1-0.56)/100))
