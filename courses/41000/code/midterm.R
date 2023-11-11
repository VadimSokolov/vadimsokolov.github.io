library(car) # Library contxaining the dataset.
library(ggplot2) # Library to create some nice looking graphs.
library(MASS) # Library for our box-cox transform down the end.
setwd("~/d/slides_2019/41000/")

mod1 = lm(income ~ education , data = Prestige)
summary(mod1)
plot(mod1, which = 1)

plot(income ~ education, data = Prestige)
plot(log(income) ~ log(education), data = Prestige)
plot(log(income) ~ education, data = Prestige)

mod1 = lm(income ~ prestige *education, data = Prestige)
summary(mod1)
plot(mod1, which = 1, cex.sub=2)
plot(education ~ prestige, data = Prestige)

# utils$save_pdf("fig/","prestige")
