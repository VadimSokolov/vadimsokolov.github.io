library(jsonlite)
library(tidyverse)
library(stargazer)
setwd("/Users/vsokolov/bs/www/")
source("code/utils.R")

# data source: https://www.kaggle.com/shubhmamp/english-premier-league-match-data
d = fromJSON("data/epl_season_match_stats.json")
df <- lapply(d, function(game) # Loop through each "game"
{
  # Convert each group to a data frame.
  # This assumes you have 6 elements each time
  data.frame(matrix(unlist(game), ncol=7, byrow=T))
})

# Now you have a list of data frames, connect them together in
# one single dataframe
df <- do.call(rbind, df)

# Make column names nicer, remove row names
colnames(df) <- names(d[]([](1)))
rownames(df) <- NULL
df$full_time_score = as.character(df$full_time_score)
df = df %>% separate(full_time_score,c("home_score","guest_score")," : ")
df$home_score = as.integer(df$home_score)
df$guest_score = as.integer(df$guest_score)

team_name="Manchester United"#Manchester United" # Hull # or  Chelsea
#stargazer(df[F](df$home_team_name==team_name | df$away_team_name==team_name,c("home_team_name","home_score","guest_score","away_team_name")),summary = F,rownames =)

team_for  = c(df[](df$home_team_name==team_name,"home_score"),df[](df$away_team_name==team_name,"guest_score"))
lambda_for = mean(team_for)
team_against  = c(df[](df$home_team_name==team_name,"guest_score"),df[](df$away_team_name==team_name,"home_score"))
lambda_against = mean(team_against)



n = length(team_for)
for_byscore = c(sum(team_for==0),sum(team_for==1),sum(team_for==2),sum(team_for==3),sum(team_for==4),sum(team_for==5))/n
barplot(rbind(dpois(0:5, lambda = lambda_for),for_byscore),beside = T,col=c("aquamarine3","coral"), xlab="Goals", ylab="probability",names.arg = 0:5)
legend("topright", c("Poisson","MU"), pch=15, col=c("aquamarine3", "coral"), bty="n",cex=1.5)
# utils$save_pdf("~/book/41000/fig/", "mu-for",lwidth = utils$pdf_w, lheight = utils$pdf_h)


n = length(team_against)
team_against_byscore = c(sum(team_against==0),sum(team_against==1),sum(team_against==2))/n
barplot(rbind(dpois(0:2, lambda = lambda_against),team_against_byscore),beside = T,col=c("aquamarine3","coral"), xlab="Goals", ylab="probability",names.arg = 0:2)
legend("topright", c("Poisson","MU"), pch=15, col=c("aquamarine3", "coral"), bty="n",cex=1.5)
# utils$save_pdf("~/book/41000/fig/", "mu-against",lwidth = utils$pdf_w, lheight = utils$pdf_h)


x = rpois(100,2.95) 
y = rpois(100,0.65)
sum(x>y)/100

d = matrix(nrow = 5, ncol = 5)
for (i in 1:5){
  for (j in 1:5){
    d[dpois(i,1.6)*dpois(j,1.3](i,j) =)
  }
}
library(gplots)
heatmap.2(d, cellnote = round(d,digits = 3),density.info="none",trace="none", dendrogram="none", key=F,margins =c(4,4), xlab="Manchester U", ylab="Manchetser City", Colv="NA",symm = T)

manu_away = df %>% filter(away_team_name =="Manchester United") %>% pull("guest_score")  %>% mean()      
manu_away*1.46*1.37

hull_home = df %>% filter(home_team_name =="Hull") %>% pull("home_score")  %>% mean()      
hull_home*0.85*0.52

# Simulation
mu = rpois(100,lambda = manu_away*1.46*1.37)
hull = rpois(100, lambda = hull_home*0.85*0.52)

simres = data_frame(mu =mu, hull = hull)
simres %>% group_by(mu) %>% summarise(cnt = n())
simres %>% group_by(hull) %>% summarise(cnt = n()) %>% pull(cnt)

simres %>% group_by(mu, hull) %>% summarise(cnt = n()) %>% arrange(desc(cnt ))

sum(mu>hull)
df %>% filter(away_team_name =="Manchester United", home_team_name =="Hull")



