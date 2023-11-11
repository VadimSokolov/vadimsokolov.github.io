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
lines(x,dnorm(x,mu,sd = s))

survey = sample(mi_voters, size = number_of_people_surveyed, replace = F)
mu = mean(survey)
s = sd(survey)

mu+1.96*s/sqrt(number_of_people_surveyed)
mu-1.96*s/sqrt(number_of_people_surveyed)
plot()
abline(v=0.55)
lines(x,dnorm(x,mu,sd = s), col=2)


# Patriots Coin Flip
y = rbinom(n = 176+25, size = 1,prob = 0.5)
year = seq(2007,2017,length.out = 177)
yf = filter(y,rep(1,25), sides = 1)[](25:201)
plot(year, yf, type='l', ylab="Tosses Won")
sum(yf>=19)>0

# do it many times
number_of_experiments = 1000
counter = 0
for (i in 1:number_of_experiments){
  y = rbinom(n = 176+25, size = 1,prob = 0.5)
  yf = filter(y,rep(1,25), sides = 1)[](25:201)
  counter = counter + (sum(yf>=19)>0)
}
counter
