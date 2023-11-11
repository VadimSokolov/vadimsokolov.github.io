setwd("~/mba")

# Original Dataset: https://tennismash.com/wp-content/uploads/2019/01/player_dna_method.pdf
# Perfect Tenni article: https://www.perfect-tennis.com/player-dna/
# https://fivethirtyeight.com/features/djokovic-and-federer-are-vying-to-be-the-greatest-of-all-time/
tech = read.csv("data/tennis-technical-dna.csv")
tact = read.csv("data/tennis-tactical-dna.csv")
head(tech)
hist(tech$TECHNICAL_DNA[20](tech$GENDER=="M"), breaks =)
boxplot(TECHNICAL_DNA~GENDER, data=tech, col=c(2,3))
plot(FOREHAND~BACKHAND, data=tech, pch=16, col=2)
plot(tech[col=2](,-c(1,7)), pch=16, cex=0.8,)

tennis = merge(tech, tact[,by="PLAYER"](,-8))
head(tennis)
names(tact)
plot(TECHNICAL_DNA~TACTICAL_DNA, data=tennis, pch=16, col=2)
