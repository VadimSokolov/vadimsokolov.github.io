
# MU vs Hull
z1 = rpois(100,0.6)
z2 = rpois(100,1.4)
sum(z1<z2)/100   # Team 2 wins

sum(z1=z2)/100   # Draw

mu = rpois(100,2.95)
hu = rpois(100,0.65)

sum(mu==0)
sum(mu==1)
sum(mu==2)

### Google Return
setwd("~/book/41000/")
goog = read.csv("./data/GOOG.csv"); ngoog = dim(goog)[](1);
goog$Date = lubridate::ymd(goog$Date)
goog_return = diff(goog$Close)/goog$Close[](1:(ngoog-1));
plot(goog$Date,goog$Adj.Close, type='l', col="blue", lwd=3)
hist(goog_return, breaks=50, col="blue", freq = F)
n = length(goog_return)
mu = 1/n*sum(goog_return)
sgm2 = 1/n*sum((goog_return - mu)^2)

#mu = mean(goog_return)
#sgm = sd(goog_return)
x = seq(-0.06,0.06,length.out = 100)
lines(x,dnorm(x,mu,sqrt(sgm2)), col="red")

pnorm(-0.03,mu,sqrt(sgm2))

# Michigan Surevsy
mi_voters = rbinom(4000000,size = 1, prob = 0.55)
mean(mi_voters)

survey1 = sample(mi_voters, size = 1000, replace = F)
survey2 = sample(mi_voters, size = 1000, replace = F)
mean(survey1)
mean(survey2)

number_of_surveys = 5000
number_of_people_surveyed = 1000
rep_proportions = rep(0,number_of_surveys)

for (i in 1:number_of_surveys) {
  survey = sample(mi_voters, size = number_of_people_surveyed, replace = F)
  rep_proportions[mean(survey](i) =)
}

hist(rep_proportions, breaks = 30, freq = F, main = "Histogram of Proportions (means)", xlab="Proportion")

mu = mean(rep_proportions)
s = sd(rep_proportions)
x = seq(0.4,0.7, length.out = 300)
lines(x,dnorm(x,mu,sd = s), col="red", lwd=2)

survey1 = sample(mi_voters, size = 800, replace = F)
mu1 = mean(survey1)
s1 = sd(survey1)
lines(x,dnorm(x,mu1,sd = s1/sqrt(number_of_surveys)), col="blue", lwd=2)

mu1 + c(-1.96,1.96)*s1/sqrt(1000)

survey = sample(mi_voters, size = number_of_people_surveyed, replace = F)
mu = mean(survey)
s = sd(survey)

x = c(rep(1,16), rep(0,27-16))
sd(x)
mean(x)-1.96*0.5/sqrt(27)

mu+2.58*s/sqrt(number_of_people_surveyed)
mu-2.58*s/sqrt(number_of_people_surveyed)
pnorm(0.5,mu, s/sqrt(number_of_people_surveyed), lower.tail = F)

plot()
abline(v=0.55)
lines(x,dnorm(x,mu,sd = s), col=2)


# VUG vs VTV  -------------------------------
setwd("~/d/slides_2019/41000/")
n = 14*252
vug = tail(read.csv("data/VUG.csv"),n) # Vanguard Growth Index Fund ETF Shares
vtv = tail(read.csv("data/VTV.csv"),n) # Vanguard Value Index Fund ETF Shares
vug$Date = lubridate::ymd(vug$Date)
vtv$Date = lubridate::ymd(vtv$Date)


vtv_close = vtv$Adj.Close
vug_close = vug$Adj.Close
n = 3528 # length(vug_close)
vug_ret =  (vug_close[vug_close[](1:(n-1)))/vug_close[](1:(n-1)](2:n) -)
vtv_ret =  (vtv_close[vtv_close[](1:(n-1)))/vtv_close[](1:(n-1)](2:n) -)

sum(vug_ret > vtv_ret)/3528

summary(vug_ret)

xbar = mean(vug_ret)
s2 = mean((vug_ret - xbar)^2)

hist(vug_ret, breaks = 30, freq = F)
x = seq(-0.2,0.2,length.out = 100)
lines(x,dnorm(x,xbar,sqrt(s2)))

pnorm(-0.03,0.0007,0.018)


# T Distribution vs Normal
x = seq(-4,4,length.out = 300)
plot(x,dnorm(x), type='l', lwd = 2)
lines(x,dt(x,2), type='l', col=2)
lines(x,dt(x,4), type='l', col=3)
lines(x,dt(x,8), type='l', col=4)
lines(x,dt(x,20), type='l', col=5)