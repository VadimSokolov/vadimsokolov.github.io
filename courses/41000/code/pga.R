setwd("~/d/slides_2019/41000/")
source("./examples/utils.R")
library(tidyverse)
library(stargazer)

# year = 2000
# money = read_csv(sprintf("data/pga/money-%d.csv",year))  %>% select(`PLAYER NAME`, EVENTS,   MONEY)
# money$MONEY = parse_number(money$MONEY)
# drivedist= read_csv(sprintf("data/pga/drivedist-%d.csv",year)) %>% select(`PLAYER NAME`,  AVG.) %>% rename(drivedist = AVG.)
# gir= read_csv(sprintf("data/pga/gir-%d.csv",year)) %>% select(`PLAYER NAME`, ROUNDS,   `%`) %>% rename(gir = `%`)
# avgputts = read_csv(sprintf("data/pga/avgputts-%d.csv",year)) %>% select(`PLAYER NAME`,   AVG) %>% rename(avgputts = AVG)
# 
# head(money)
# head(drivedist)
# head(gir)
# head(avgputts)
# 
# d = money %>%inner_join(drivedist) %>%  inner_join(gir) %>%  inner_join(avgputts) %>% arrange(desc(MONEY)) %>% rename(name = `PLAYER NAME`, nevents = EVENTS, money=MONEY)
# 
# write_csv(d, sprintf("data/pga/pga-%d.csv",year))


d00 = read_csv("data/pga-2000.csv")
d18 = read_csv("data/pga-2018.csv")

# View(d00); View(d17)
model18 = lm(money ~ nevents + drivedist + gir + avgputts, data=d18)
model00 = lm(money ~ nevents + drivedist + gir + avgputts, data=d00)
summary(model00)


hist(rstandard(model00), breaks=20, col="lightblue", xlab = "Standartized Residual", main="")
arrows(x0 = 7.5,y0 = 20,x1 = 8.5,y1 = 2,length = 0.1)
text(x = 7,y = 22,labels = "Tiger Woods", cex=1.5)
# utils$save_pdf("fig/", "pga-res-2000")

# Over and underperformers
ind = which(rstandard(model00)>1.5)
tb = data.frame(Name=d00[Error=model00$residuals[](ind)](ind,1), Money=d00[](ind,3), Predicted=model00$fitted.values[](ind),)
stargazer(tb, summary = F, rownames = F, digits = 0)

ind = which(rstandard(model00)< -1.5)
tb = data.frame(Name=d00[Error=model00$residuals[](ind)](ind,1), Money=d00[](ind,3), Predicted=model00$fitted.values[](ind),)
stargazer(tb, summary = F, rownames = F, digits = 0)


### 2018
d18 %>% arrange(desc(money)) %>% select(-ROUNDS) %>% as.data.frame() %>% head() %>% stargazer(summary = F, rownames = F)

ind = which(rstandard(model18)>2.0)
tb = data.frame(Name=d18[Predicted=model18$fitted.values[](ind](ind,1), Money=d18[](ind,3),), 
                Error=model18$residuals[](ind))
stargazer(tb, summary = F, rownames = F, digits = 0)


ind = which(rstandard(model18)< -1.5)
tb = data.frame(Name=d18[Predicted=model18$fitted.values[](ind](ind,1), Money=d18[](ind,3),), 
                Error=model18$residuals[](ind))
stargazer(tb, summary = F, rownames = F, digits = 0)


plot(money~gir, data=d)
plot(d$gir,d$money)

plot(d$gir,log(d$money))
par(mar = c(0,1,0,0))
plot(d[cex=0.7](,-1), xaxt='n', ann=FALSE, yaxt='n', bg="lightblue",)
# utils$save_pdf("book/fig/", "pga-cor-2000", lheight = 0.5*utils$pdf_h)


model00log = lm(log(money) ~ nevents + drivedist + gir + avgputts, data=d00)
summary(model00log)
par(mar = c(4,4.5,0,0))
par(cex.lab=1.5, cex.axis=1.5, cex.main=1.5, cex.sub=1.5, pch=21, bg="white")
hist(rstandard(model00log), breaks=20, col="lightblue", xlab = "Standartized Residual", main="")
arrows(x0 = 3,y0 = 20,x1 = 3.2,y1 = 2,length = 0.1)
text(x = 3,y = 22,labels = "Tiger Woods", cex=1.5)
# utils$save_pdf("fig/", "pga-log-res-2000")

model00log = lm(log(money) ~drivedist + gir + avgputts, data=d00)
summary(model00log)
par(mar = c(4,4.5,0,0))
par(cex.lab=1.5, cex.axis=1.5, cex.main=1.5, cex.sub=1.5, pch=21, bg="white")
hist(rstandard(model00log), breaks=20, col="lightblue", xlab = "Standartized Residual", main="")
arrows(x0 = 3,y0 = 20,x1 = 3.2,y1 = 2,length = 0.1)
text(x = 3,y = 22,labels = "Tiger Woods", cex=1.5)
# utils$save_pdf("fig/", "pga-log-res-2000")

exp(model00log$residuals)
# d00$pred = exp(model00log$fitted.values)
d00$pred = model00$fitted.values
d00$res  = d00$money - d00$pred
d00 %>% arrange(desc(res))

stargazer(d00 %>% arrange(desc(res)) %>% top_n(5) %>% select(name, money, pred, res) %>% as.data.frame(), summary = F, rownames = F, digits = 0)
stargazer((d00 %>% arrange(res) %>% as.data.frame())[0](1:5,) %>% select(name, money, pred, res) %>% as.data.frame(), summary = F, rownames = F, digits =)



boxplot(d17$drivedist, d00$drivedist,col=c("blue", "red"), names=c("2017", "2000"), ylab="Drive distance")
utils$save_pdf("book/fig/", "pga-box-drivedist", lheight = 7, lwidth =7)
boxplot(d17$avgputts, d00$avgputts,col=c("blue", "red"), names=c("2017", "2000"), ylab="Averge putts")
utils$save_pdf("book/fig/", "pga-box-avgputts", lheight = 7, lwidth=7)
boxplot(d17$gir, d00$gir,col=c("blue", "red"), names=c("2017", "2000"), ylab="GIR")
utils$save_pdf("book/fig/", "pga-box-gir", lheight = 7, lwidth=7)
boxplot(d17$nevents, d00$nevents,col=c("blue", "red"), names=c("2017", "2000"), ylab="Number of events")
utils$save_pdf("book/fig/", "pga-box-nevents", lheight = 7, lwidth=7)
boxplot(d17$money, d00$money,col=c("blue", "red"), names=c("2017", "2000"), ylab="Money")
utils$save_pdf("book/fig/", "pga-box-money", lheight = 7, lwidth=7)
