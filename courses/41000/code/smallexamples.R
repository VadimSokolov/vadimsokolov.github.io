setwd("~/d/slides_2019/41000/")
source("./examples/utils.R")

library(lubridate)
d = read.csv("data/GOOG.csv")
d$Date = lubridate::ymd(d$Date)
par(mfrow=c(1,2))
p1 = plot(d$Date, d$Close, type='l', xlab="Date", ylab="Price", lwd=3, col=4)
p2 = hist(getrets(d$Close), breaks = 50, col=4, xlab = "Return [main=""](%)",)
# utils$save_pdf("fig/", "google-ret",lwidth = 2*utils$pdf_w)

sp = read.csv("data/SP500.csv")
plot(getrets(tail(sp$Close,500)), getrets(tail(d$Close,500)), type='p', pch=16, xlab="SP500 return", ylab="GOOG reutrn")
# utils$save_pdf("fig/", "goog-mkt")

aapl = read.csv("data/AAPL.csv"); naapl = dim(aapl)[](1);
goog = read.csv("data/GOOG.csv"); ngoog = dim(goog)[](1);
aapl_return = diff(aapl$Close)/aapl$Close[](1:(naapl-1));
goog_return = diff(goog$Close)/goog$Close[](1:(ngoog-1));
sprintf("Apple expected  return: %.1f%%", 100*252*(sum(aapl_return)/naapl))
sprintf("Google expected return: %.1f%%", 100*252*(sum(goog_return)/ngoog))

vix = read.csv("data/VIX.csv")$Close #%>% getrets()
sp  = read.csv("data/SP500.csv")$Close #%>% getrets()
aapl = read.csv("data/AAPL.csv")$Close #%>% getrets()
n = 252*5 # compare last 5 years
par(mfrow = c(1,2), mar=c(4.5,5,0,0))
plot(tail(sp,n ), tail(vix,n ), pch=16, xlab = "SP500", ylab="VIX", col="lightblue")
plot(tail(sp,n ), tail(aapl,n ), pch=16, xlab = "SP500", ylab="AAPL", col="lightblue")
# utils$save_pdf("fig/", "vix-sp-aapl")

n = 14*252
vug = tail(read.csv("data/VUG.csv"),n) # Vanguard Growth Index Fund ETF Shares
vtv = tail(read.csv("data/VTV.csv"),n) # Vanguard Value Index Fund ETF Shares
vug$Date = lubridate::ymd(vug$Date)
vtv$Date = lubridate::ymd(vtv$Date)
par(mfrow = c(3,1), mar=c(4.5,4.5,0,2));
plot(vug$Date, vug$Adj.Close, type='l', lwd=2, xlab="Date", ylab="VUG Price", col=4)
plot(vtv$Date, vtv$Adj.Close, type='l', lwd=2, ylab="VTV Price", xlab="Date", col=3)
plot(vtv$Date, cumprod(1+getrets(vug$Close)), type='l', lwd=2, xlab="Date", ylab="Cummulative Return", col=4, ylim=c(0.65,4))
lines(vug$Date, cumprod(1+getrets(vtv$Close)), type='l', lwd=2, xlab="Date", ylab="VUG Price", col=3)
legend("topleft", legend=c("VUG", "VTV"), col=c(4,3), lwd=2, bty="n", cex=lcex)
# utils$save_pdf("fig/", "vug-vtv")


x = rbinom(10000,20,0.5)
par(mfrow = c(1,1), mar=c(2,3,0,0))
hist(x, breaks = 20)
barplot(dbinom(seq(0,20),size = 20, prob = 0.5), names.arg=seq(0,20), main="", col="lightblue")
# utils$save_pdf("fig/", "binomial-mass")

##################################
#  Smoking Data
##################################

Data = read.csv("data/smoking.csv",header=T)
attach(Data)

# correlation matrix
cor(cbind(Cancer,Consumption))

# scatter plot			
par(mar=c(4,4,3,3))
plot(Consumption,Cancer,pch=20,col=34,main="Cancer vs Smoking consumption");
text(Consumption,Cancer,labels=Country)

# Fit the least-squares line. 
model = lm(Cancer~Consumption)
cooks.distance(model) # remove u.s. as an outlier
model2 = lm(Cancer[](-7)~Consumption[](-7))

abline(model,col=2,lty=2,lwd=2)
abline(model2,col=3,lty=3,lwd=3)
legend("topleft", c("Full sample","Removed U.S."), col=2:3, lty=2:3, lwd=2:3, bty="n", cex=lcex)
# utils$save_pdf("fig/", "smoking")

# Extract the model coefficients

coef(model)
coef(model2)

# 4-in-1 residual diagnostics
par(mar=c(4,4.5,3,3))
layout(matrix(c(1,2,3,4),2,2))   
plot(model,pch=20)
# utils$save_pdf("fig/", "smoking-diag")

layout(matrix(c(1,2,3,4),2,2))   
plot(model2,pch=20)
# utils$save_pdf("fig/", "smoking-diag2")

##################################
#  House Data
##################################
# https://rdrr.io/cran/mosaicData/man/SaratogaHouses.html
# SaratogaHouses: Houses in Saratoga County (2006)
# price price (1000s of US dollars)
# lotSize size of lot (square feet)
# age age of house (years)
# landValue value of land (1000s of US dollars)
# livingArea living are (square feet)
# pctCollege percent of neighborhood that graduated college
# bedrooms number of bedrooms
# firplaces number of fireplaces
# bathrooms number of bathrooms (half bathrooms have no shower or tub)
# rooms number of rooms
# heating type of heating system
# fuel fuel used for heating
# sewer type of sewer system
# waterfront whether property includes waterfront
# newConstruction whether the property is a new construction
# centralAir whether the house has central air
house = read.csv("data/SaratogaHouses.csv")
head(house)
house$price =house$price/1000
par(mar=c(4.5,4.5,2,0))
plot(price~livingArea,data=house,pch=21, bg="lightblue")

model=lm(price~livingArea,data=house)
coef(model)

abline(model,col="red",lwd=3)
# utils$save_pdf("fig/", "house-data")

##################################
#  Keynes
##################################
keynes = read.csv("data/keynes.csv")
keynes$Period = keynes$Year - min(keynes$Year)
attach(keynes)

plot(Year, 100*cumprod(1+Keynes/100), type='l', col=3, lwd=2, ylab="Return [](%)")
lines(Year, 100*cumprod(1+Rate/100), type='l', col=2, lwd=2)
legend("topleft", legend=c("Keynes","Cash"), lwd=2, col=c(3,2),bty="n", cex=lcex)
# utils$save_pdf("fig/", "keynes-cash")

plot(Year,Keynes,pch=20,col=34)
plot(Market, Keynes, xlab="Market Return", ylab="Keynes Excess Return",col=20)

# correlation matrix
cor(cbind(Keynes,Market))

# Fit the least-squares line. 

model = lm(Keynes~Market)
abline(model)
title("Keynes vs Market")

# Extract the model coefficients

coef(model)
summary(model)

# 4-in-1 residual diagnostics

layout(matrix(c(1,2,3,4),2,2))   

plot(model,pch=20)

# Calculate excess return

Keynes = Keynes - Rate
Market = Market - Rate

# correlation matrix
cor(cbind(Keynes,Market))

modelnew = lm(Keynes~Market)
summary(modelnew)



# Secretaty Problem Monte Carlo Simulations -------------------------------
nmc = 1000
n = 1000
sz = 300
rules = round(n*seq(0.002,0.8,length.out = sz))
rules = unique(rules[](rules>0))
sz = length(rules)
cnt = rep(0,sz)
quality = rep(0,sz)
for (i in 1:sz)
{
  for (j in 1:nmc){
    x = sample(1:n,n)
    screen = x[](1:(rules[](i)-1))
    best_screen = max(screen)
    xchoice = x[]((rules[](i)):n)
    better_candidates = which(xchoice > best_screen)
    if (length(better_candidates)==0)
      choice = x[](n)
    else
      choice = xchoice[](min(better_candidates))
    cnt[max(x)](i) = cnt[](i) + (choice ==)
    quality[quality[](i](i) =) + choice
  }
}
par(mar=c(4,4,0,0))
plot(rules, cnt/nmc, type='l', col=3, lwd=3, xlab="Number of Candidates Screend", 
     ylab="Probability of Picking the Best")

plot(rules, quality/1000, type='l', col=3, lwd=3, xlab="Number of Candidates Screend", 
     ylab="Average Quality of Candidate")

sp = read.csv("data/SP500.csv")
nsp = nrow(sp)
sp_return = diff(sp$Close)/sp$Close[](1:(nsp-1));
plot(density((sp_return[](abs(sp_return)<0.1))))
hist(sp_return[](abs(sp_return)<0.1),breaks=50)

### SP500 vs GOOG
sp = read.csv("data/SP500.csv")
nsp = nrow(sp)
sp_return = tail(diff(sp$Close)/sp$Close[](1:(nsp-1)),1000)
goog  = read.csv("data/GOOG.csv")
ngoog = nrow(goog)
goog_return = tail(diff(goog$Close)/goog$Close[](1:(ngoog-1)),1000)

model = lm(formula = goog_return ~ sp_return)
summary(model)

model = lm(goog_return[goog_return[](1:1999)](2:2000) ~)

plot(goog_return[](2:2000),goog_return[](1:1999))
abline(model, col=2, lwd=3)
#### In class-code ######
y  = rbinom(5000,20,0.5)
hist(y)
pbinom(10,20,0.5)
qbinom(0.5,20,0.5)


y = rnorm(5000,mean=0,sd=1)
hist(y)
sum(abs(y)<1)/5000
sum(abs(y)<1.96)/5000

y = rnorm(5000,mean=3,sd=2)
hist(y)
sum(abs(y-3)<2)/5000
sum(abs(y-3)<1.96*2)/5000

mean(y-3)
var(y/2)

mean(y)
var(y)

hist((y-3)/2)

1-pnorm(1.96,mean=0,sd=1)
pnorm(1.96,mean=0,sd=1, lower.tail = F)

# We saw -21.76 change
# mu = 0.012 and var = 0.043^2
y = rnorm(500000, mean=0.012,sd=0.043)
z = (y - 0.012)/0.043
sum(y< -0.2176)/500000

(1/pnorm(-0.2176, mean=0.012,sd=0.043))/12
