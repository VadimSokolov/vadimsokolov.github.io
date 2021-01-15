### Google Algorithm Example
p1 = 1755/2500
p2 = 1818/2500
v1 = p1*(1-p1)/2500
v2 = p2*(1-p2)/2500

# confidence interval
s = sqrt(v1 + v2)
(p1 - p2) + 1.96*s
(p1 - p2) - 1.96*s

# t-score
(p1 - p2)/s

# p-value (H0: difference is greater than 0)
pnorm(-1.973632)

# p-value (H0: difference is not equal to 0)
pnorm(-1.973632) + pnorm(1.973632,lower.tail = F)
# p-value (H0: difference is less than 0)
pnorm(-1.973632, lower.tail = F)


# We do not want Yates' continuity correction to be applied to we set correct = F
prop.test(c(1755,1818),c(2500,2500), alternative = "two.sided", correct = F)
prop.test(c(1755,1818),c(2500,2500), alternative = "less", correct = F)
prop.test(c(1755,1818),c(2500,2500), alternative = "greater", correct = F)


### Pfizer
p1=77/6000000
p2=11/1500000
v1=p1*(1-p1)/6000000
v2=p2*(1-p2)/1500000
S=sqrt(v1+v2)
p1-p2+1.96*(S)
p1-p2-1.96*(S)

prop.test(x=c(77, 11), n=c(6000000, 1500000), correct = F)

### Electronic Arts
abtestfunc <- function(ad1, ad2){
  sterror1 = sqrt( ad1[1] * (1-ad1[1]) / ad1[2] )
  sterror2 = sqrt( ad2[1] * (1-ad2[1]) / ad2[2] )
  minmax1 = c((ad1[1] - 1.28*sterror1) * 100, (ad1[1] + 1.28*sterror1) * 100)
  minmax2 = c((ad2[1] - 1.28*sterror2) * 100, (ad2[1] + 1.28*sterror2) * 100) 
  print( round(minmax1,2) )
  print( round(minmax2,2) )
}

site1 = c(.40, 500) # pink
site2 = c(.30, 550) # black 
abtestfunc(site1, site2)

### Lord Rayleigh
a = c(2.31017,2.30986)
b = c(2.30143, 2.29890)

t.test(a,b, var.equal = T)

### Cookie Cats
### Demo: https://www.youtube.com/watch?v=GaP5f0jVTWE&feature=youtu.be
# now we can read the data
d = read.csv("data/cookie_cats.csv")

head(d) # show first 6 rows

# -  `userid`: unique user ID
# -  `version`: versions with different gates preventing the player’s progress, after 30 levels or after 40, these are recorded as gate_30 and gate_40
# - `sum_gamerounds`: number of rounds played by each unique user during the first 14 days after install
# - `retention_1`:  player is still active after 1 day
# - `retention_7`:  player is still active after 7 days

dim(d) # data has 90189 rows and 5 columns

# Make sure we have two distinct versions 
unique(d$version)



group_30 = d[d$version == "gate_30",] #rows when gate_30 users are selected
group_40 = d[d$version == "gate_40",] #rows when gate_40 users are selected

# Count number of unique users in each group
nrow(group_30) # number of rows
nrow(group_40) # number of rows

# Count average retention after 1 day by group
mean(group_30$retention_1) # 44.8%
mean(group_40$retention_1) # 44.2%

# Count average retention after 7 day by group
mean(group_30$retention_7) 
mean(group_40$retention_7) 

par(mar=c(4,4,0,1))
hist(d$sum_gamerounds[d$sum_gamerounds<100], breaks=25, xlab="Game Rounds", ylab="Number of Users", main="", col="lightblue")

# Count average retention after 7 days by group
mean(group_30$retention_7) 
mean(group_40$retention_7) 

# Count average numper of rounds by group
mean(group_30$sum_gamerounds) # 52.5
mean(group_40$sum_gamerounds) # 51.3

# We put our code to calculate a confidence interval inside a function
confidence_interval = function(x) 
{
  n = length(x)
  xbar = sum(x)/n
  sigma2 = sum((x-xbar)^2)/n
  sigma = sqrt(sigma2)
  SEM = sigma/sqrt(n)
  
  cat(sprintf("\n\nNumber of samples is %d\n", n))
  cat(sprintf("xbar is %.2f\n", xbar))
  cat(sprintf("sigma is %.2f\n", sigma))
  cat(sprintf("SEM is %.3f\n", SEM))
  cat(sprintf("The confidence interval is [%.3f,  %.3f]", xbar-1.96*SEM, xbar+1.96*SEM))
}

confidence_interval(group_30$retention_1)
confidence_interval(group_40$retention_1)

confidence_interval(group_30$retention_7)
confidence_interval(group_40$retention_7)

confidence_interval(group_30$sum_gamerounds)
confidence_interval(group_40$sum_gamerounds)




