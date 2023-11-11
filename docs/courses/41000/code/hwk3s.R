##  Business Statistics: Hwk3
##---------------------------------

# set your working directory
# setwd("~/....") 

#------------------------------
#   Buffett vs Keynes
#------------------------------

buffett = read.csv("http://vsokolov.org/courses/41000/data/buffett.csv",header=T)
attach(buffett)


# Plot the data

plot(Market, Buffett, xlab="Market Return", ylab="Buffett Return",pch=20,bty='n')
legend(x="topleft",legend=c("Buffett","Market"),pch=20,col=c(2,4),bty="n")

# correlation matrix
cor(cbind(Buffett,Market))

# Fit the least-squares line and superimpose this line on the plot

model = lm(Buffett~Market)
abline(model,col="red",lwd=3)
title("Buffett vs Market")


# Extract the model coefficients 

coef(model)
summary(model)

# Improvement in Fit

sd(model$residuals)
sd(Buffett)

# Prediction of portfolios 

# Market return = 10%
newdata = data.frame(10) 
colnames(newdata) = "Market"
predict(model,newdata)
# sum(coef(model)*c(1,10))

# Market return = -10%
newdata2 = data.frame(-10) 
colnames(newdata2) = "Market"
predict(model,newdata2)
# sum(coef(model)*c(1,-10))


# To remove datapoint 10
# buffett_10 = buffett[](-10,)

detach(buffett)


#-------------------------------------
#  Keynes Data
#-------------------------------------

keynes = read.csv("http://vsokolov.org/courses/41000/data/keynes.csv",header=T)
attach(keynes)

# Plot the data

plot(Year,Keynes,pch=20,col="dark grey",type='l',bty='n')

plot(Market, Keynes, xlab="Market Return", ylab="Keynes Excess Return",col=20,pch=20,bty='n')

# correlation matrix
cor(cbind(Keynes,Market))

# Fit the least-squares line. 

model = lm(Keynes~Market)
abline(model,col="red",lwd=3)
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

# Diagnostics

summary(modelnew)

# Prediction of portfolios 

# Market return = 10%

sum(coef(model)*c(1,10))

# Market return = -10%

sum(coef(model)*c(1,-10))


detach(keynes)


#------------------------------
#   Diamond Pricing
#------------------------------

diamond = read.csv("http://vsokolov.org/courses/41000/data/diamond.csv",header=T)
colnames(diamond) = c("Weight", "Price")
diamond$Weight = as.numeric(diamond$Weight)
diamond$Price = as.numeric(diamond$Price)

# Run a regression

fit = lm(Price~Weight,data = diamond)
summary(fit)

# Plot Price versus Weight

plot(Price~Weight,data = diamond,
     xlab="Weight (carats)",ylab = "Price (Singapore dollars)",
     main= "Bivariate Fit of Price (Singapore dollars) By Weight (carats)",
     xaxs="i", yaxs="i",pch=20,bty='n')

abline(fit,col="red",lwd=2)

# Plug-in prediction

# Weight = 0.25

sum(coef(fit)*c(1,0.25))

# Weight = 1

sum(coef(fit)*c(1,1))



#------------------------------
#   NFL Salaries
#------------------------------

salary = read.csv("http://vsokolov.org/courses/41000/data/NFLsalary.csv", header = TRUE, stringsAsFactors = T)
salary$Conf = as.factor(salary$Conf)

# attach the dataset 
attach(salary)

# Plot a boxplot to compare salaries of the NFC to AFC.
boxplot(Salary~Conf, data=salary,main="Team Salary by Conference",  ylab="Salary ($1,000s)")

# Dummy coding (dummy code the "Conf" variable into NFC = 1 and AFC = 0)
dConf = as.numeric(Conf) - 1

# Routine analysis
mean(dConf)
sd(dConf)
cor(dConf, Salary)

# Linear regression wit a dummy variable
model = lm(Salary ~ QB + dConf) 
# model = lm(Salary ~ QB + Conf)  #produces the same regression result.
summary(model)

detach(salary)

