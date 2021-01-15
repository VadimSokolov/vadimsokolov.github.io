# HW1
# pnorm(5,mean = 10,sd = 3)

y = rnorm(n = 5000, mean = 10, sd = 3)

sum(y<=5)/5000

pbinom(10,size = 120,prob = .0466,lower.tail = F)
1-pnorm(10,.0466*120,sqrt(120*.0466*(1-.0466)))


1 - pbinom(10, 120, .0466)

pnorm(-0.03,0.0007, 0.018)

1/sqrt(2500)

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
goog = read.csv("data/GOOG.csv"); ngoog = dim(goog)[1];
goog$Date = lubridate::ymd(goog$Date)
goog_return = diff(goog$Close)/goog$Close[1:(ngoog-1)];
plot(goog$Date,goog$Adj.Close, type='l', col="blue", lwd=3)
hist(goog_return, breaks=50, col="blue")

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
  rep_proportions[i] = mean(survey)
}

hist(rep_proportions, breaks = 30, freq = F, main = "Histogram of Proportions (means)", xlab="Proportion")

mu = mean(rep_proportions)
s = sd(rep_proportions)
x = seq(0.4,0.7, length.out = 300)
lines(x,dnorm(x,mu,sd = s))

survey = sample(mi_voters, size = number_of_people_surveyed, replace = F)
mu = mean(survey)
s = sd(survey)

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
vug_ret =  (vug_close[2:n] - vug_close[1:(n-1)])/vug_close[1:(n-1)]
vtv_ret =  (vtv_close[2:n] - vtv_close[1:(n-1)])/vtv_close[1:(n-1)]

sum(vug_ret > vtv_ret)/3528

summary(vug_ret)

xbar = mean(vug_ret)
s2 = mean((vug_ret - xbar)^2)

hist(vug_ret, breaks = 30, freq = F)
x = seq(-0.2,0.2,length.out = 100)
lines(x,dnorm(x,xbar,sqrt(s2)))

pnorm(-0.03,0.0007,0.018)
