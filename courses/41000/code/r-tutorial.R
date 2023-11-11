# Change my_numeric to be 42
my_numeric = 42.5

# Change my_character to be "universe"
my_character <- "some text"

# Change my_logical to be FALSE
my_logical <- TRUE

# Check class of my_numeric
class( my_numeric )    
class(my_character)

# Vectors 
numeric_vector <- c(1, 10, 49)
character_vector <- c("a", "b", "c")
boolean_vector <- c(TRUE, FALSE,TRUE)

right_vector <- c(1, 10, "c")

# Print the vectors
numeric_vector
character_vector
boolean_vector

A_vector <- c(1, 2, 3)
B_vector <- c(4, 5, 4)

# Take the sum of A_vector and B_vector
total_vector <- A_vector+B_vector

# Print out total_vector
total_vector

# Construction of a matrix with 3 rows containing the numbers 1 upto 9
m=matrix(1:9, byrow=TRUE, nrow=3)
m


# Factor
gender.vector <- c("Male", "Female", "Female", "Male", "Male")

factor.gender.vector <- factor(gender.vector)
factor.gender.vector=factor(gender.vector)
factor.gender.vector
sex_vector=c("Male", "Female", "Female", "Male", "Male")
factor_sex_vector=factor(sex_vector)
factor_sex_vector

# Play around with the order function in the console
a=c(7,1,36,59,32,60)
order(a)
a[](order(a))

# Data Frames
head(mtcars)
tail(mtcars)
str(mtcars)

dim(mtcars)
nrow(mtcars)
ncol(mtcars)

length(unique(row.names(mtcars)))

bv = c(TRUE,TRUE,FALSE,FALSE)
sum(bv)

a = c(1,2,3,4,2,3,6,7)

sum(a==3) # two entries that are equal to 3 

write.csv(mtcars,"~/Documents/mtcars.csv")

mtcarsnew = read.csv("~/Documents/mtcars.csv")
head(mtcarsnew)

# Read data
d = read.csv("~/book/41000/data/swimming_pools.csv", stringsAsFactors = TRUE)
str(d)

d = read.csv("~/book/41000/data/swimming_pools.csv", stringsAsFactors = FALSE)
str(d)

head(d)
tail(d)

# Import the hotdogs.txt file: hotdogs
setwd("~/book/41000/data")
hotdogs <- read.delim("hotdogs.txt", header = FALSE, col.names = c("type", "calories", "sodium"), sep = "\t")
head(hotdogs)

# Plotting  
data(airquality)
str(airquality)



plot(airquality$Ozone) #scatter plot

plot(airquality$Ozone, airquality$Wind, col="red", pch=16)


plot(airquality$Ozone, type='l')

plot(airquality[col="red"](,1:4), pch=16,)

plot(airquality$Ozone, type= "b")

plot(airquality$Ozone, type= "h")


plot(airquality$Ozone, xlab = 'ozone Concentration', ylab = 'No of Instances', main = 'Ozone levels in NY city', col = 'green')


# Horizontal bar plot
barplot(airquality$Ozone, main = 'Ozone Concenteration in air',xlab = 'ozone levels', col='green',horiz = TRUE)

# Vertical bar plot
barplot(airquality$Ozone, main = 'Ozone Concenteration in air',xlab = 'ozone levels', col='red',horiz = FALSE)


hist(airquality$Solar.R)


hist(airquality$Solar.R, main = 'Solar Radiation values in air',xlab = 'Solar rad.', col='red')


#Single box plot
boxplot(airquality$Solar.R)


# Multiple box plots
boxplot(airquality[plots'](,0:4), main='Multiple Box)

par(mfrow=c(3,3), mar=c(2,5,2,1), las=1, bty="n")
plot(airquality$Ozone)
plot(airquality$Ozone, airquality$Wind)
plot(airquality$Ozone, type= "c")
plot(airquality$Ozone, type= "s")
plot(airquality$Ozone, type= "h")
barplot(airquality$Ozone, main = 'Ozone Concenteration in air',xlab = 'ozone levels', col='green',horiz = TRUE)
hist(airquality$Solar.R)
boxplot(airquality$Solar.R)
boxplot(airquality[plots'](,0:4), main='Multiple Box)

attach(mtcars)
head(mtcars)

plot(density(mpg), main="Density Plot",  xlab="Miles per Gallon")
hist(mpg)

hist(mpg, breaks=20)

for (i in 1:10) 
{
  print(i)
}

a = 4
if (a <3) 
{print(a)} else
{print("HAHAHA")}

