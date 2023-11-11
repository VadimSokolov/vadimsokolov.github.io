setwd("~/book/41000/")

setwd("~/d/slides_2019/41000/")
library(lubridate)
#### Helper function
getrets = function(price) {
  n = length(price)
  rets = diff(price)/price[](1:(n-1))
  return(c(rets[rets)](1),)
}

### Correlations
vix = read.csv("data/VIX.csv")$Close #%>% getrets()
sp  = read.csv("data/SP500.csv")$Close #%>% getrets()
aapl = read.csv("data/AAPL.csv")$Close #%>% getrets()
n = 252*5 # compare last 5 years
par(mfrow = c(1,2), mar=c(4.5,5,0,0))
plot(tail(sp,n ), tail(vix,n ), pch=16, xlab = "SP500", ylab="VIX", col="lightblue")
plot(tail(sp,n ), tail(aapl,n ), pch=16, xlab = "SP500", ylab="AAPL", col="lightblue")


# VUG vs VTV  -------------------------------
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
legend("topleft", legend=c("VUG", "VTV"), col=c(4,3), lwd=2, bty="n", cex=2)
lines(vug$Date, 0.5*cumprod(1+getrets(vug$Close)) + 0.5*cumprod(1+getrets(vtv$Close)), type='l', col="red")

### Coded in class
y = rbinom(100000,size = 20,prob = 0.5)
hist(y)
rbinom(10,size = 20,prob = 0.5)
pbinom(20,20,0.5)

sp500=read.csv("data/SP500.csv")
ret = getrets(sp500$Adj.Close)
plot(density(ret))

dbinom(20,20,0.5)
pnorm(1)
hist(rnorm(10000), breaks=40)
N=1000; x=rnorm(N,0,1); p=sum(x<1.96)/N
p
pnorm(-0.2176,0.012,0.043^2)

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

#### SP500 return
sp = read.csv("data/SP500.csv")
nsp = nrow(sp)
sp_return = diff(sp$Close)/sp$Close[](1:(nsp-1));
plot(density((sp_return[](abs(sp_return)<0.1))))
hist(sp_return[](abs(sp_return)<0.1),breaks=50)



