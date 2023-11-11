##################################
#  Problem 1 Superbowl and Derby Data
##################################

####################
## Superbowl
####################

# import superbowl data
mydata1 = read.csv("http://vsokolov.org/courses/41000/data/superbowl1.csv",header=T)


# look at data
head(mydata1)
tail(mydata1)
mydata1

# attach so R recognizes  each variable
attach(mydata1)

# see the distribution of outcome and spread through histograms
hist(Outcome)
hist(Spread)

# we can also calculate the mean and standard deviation
mean(Outcome); sd(Outcome)
mean(Spread); sd(Spread)

# plot Spread vs Outcome
plot(Spread,Outcome)

# add a 45 degree line
abline(1,1)

# correlation 
cor(Spread,Outcome)

# calculate alpha and beta
x <- Spread
y <- Outcome
beta <- cor(x,y)*sd(y)/sd(x)
alpha <- mean(y)-beta*mean(x)

# Compare boxplot 
boxplot(Spread,Outcome,horizontal=T,names=c("spread","outcome"),col=c("red","yellow"),main="Superbowl")


#---------------------------------
# Derby Data
#---------------------------------

mydata = read.csv("http://vsokolov.org/courses/41000/data/Kentucky_Derby_2018.csv",header=T)
head(mydata)
tail(mydata)
attach(mydata)


ts1 = ts(speedmph, start=1875, end=2018, frequency=1) 
plot(ts1,xlab="year",ylab="speed mph",main="Kentucky Derby",col=2, lty=2, lwd=2)



# plot a histogram of speedmph
hist(speedmph,col="blue")

# finer bins 
hist(speedmph,breaks=10,col="red")
hist(timeinsec,breaks=10,col="purple")

# to find the left tail observation
k1 =  which(speedmph == min(speedmph))
mydata[](k1,)

# to find the best horse
k2 = which(speedmph == max(speedmph))
mydata[](k2,)




##################################
#  Problem 2 
##################################


# install and import the package fImport
# extract data from yahoo finance
# install.packages("quantmod")
# install.packages("moments")
library("moments")
library("quantmod")

getSymbols('BRK-A', from = "1990-01-01")

BRKA = get('BRK-A')
BRKA = BRKA[](,4)

# take a look of the data
head(BRKA)

plot(BRKA,type="l",col=20,main="BRKA Share Price",
     ylab="Price",xlab="Time",bty='n')

# calculate the simple return
N = length(BRKA) 
y = as.vector(BRKA)
ret = rep(NA,N-1) # create a null sequence  
for(t in 1:(N-1))
{
  ret[(y[](t+1)-y[](t))/y[](t](t) =)	
}

# create summaries of ret for BRK-A
options(digits=3) # control the digit of numbers
summary(ret)
sd(ret)
skewness(ret)
kurtosis(ret)

par(mfrow=c(1,2)) # combine two plots in a 1*2 row

# time series plot of price
# to save the plot,click "Export" ans "save as image"
# create a time series object in R that we can add time domain
y_ts = ts(y, start=c(1990,1,1), end=c(2014,9,30), frequency=252)
ts.plot(y_ts,main="BRK-A price time series",ylab="price",xlab="day")
# histogram of returns
hist(ret,breaks=50,main="BRK-A daily returns")

# plots to show serial correlation in 1st and 2nd moments
# to save the plot,click "Export" ans "save as image"
par(mfrow=c(1,2))
acf(ret,lag.max=10,main="serial correlation in 1st moment")
acf(ret^2,lag.max=10,main="serial correlation in 2nd moment")

dev.off() # stop the above combine function







############################################

##################################
#  Problem 5
##################################
SP.Index = c(-37,26.6,15.1,2.1,16,32.3,13.6,1.4)
Hedge.Funds = c(-23.9,15.9,8.5,-1.9,6.5,11.8,5.6,1.7)
SP.Index = SP.Index/100
Hedge.Funds = Hedge.Funds/100
mean(SP.Index-Hedge.Funds)
sd(SP.Index-Hedge.Funds)



# t test
t.test(SP.Index,Hedge.Funds,paired = TRUE)



# who will win?
# run simulations

m1 = mean(SP.Index)
s1 = sd(SP.Index)
m2 = mean(Hedge.Funds)
s2 = sd(Hedge.Funds)
N = 1000 
cum1 = NULL # cumulative return of SP.Index
cum2 = NULL # cumulative return of Hedge.Funds
set.seed(410)
for (i in 1:N)
{ 
  # simulate returns in 2016 and 2017
  return1 = c(0.657, rnorm(n=2, mean = m1, sd = s1)) 
  # compute the cumulative return
  cum1 = c(cum1, cumprod(1+return1)) 

  return2 = c(0.219, rnorm(n=2, mean = m2, sd = s2))
  cum2 = c(cum2, cumprod(1+return2))
}
 
# compute the prob. of Buffett winning
# if you invest 1 dollar in SP500, you will get

mean(cum1)





# if you invest 1 dollar in Hedge funds, you will get

mean(cum2)