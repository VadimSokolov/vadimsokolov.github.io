#' ---
#' title: "Trump Twitter analysis using the `tidyverse`"
#' author: "Adam Spannbauer and Jennifer Chunn"
#' date: "`r Sys.Date()`"
#' output: 
#'   rmarkdown::html_vignette:
#'     df_print: kable
#' vignette: |
#'   %\VignetteIndexEntry{Trump Twitter tidyverse analysis}
#'   %\VignetteEngine{knitr::rmarkdown}
#'   %\VignetteEncoding{UTF-8}
#' ---
#' 
#' This vignette is based on data collected for the 538 story entitled "The World's Favorite Donald Trump Tweets" by Leah Libresco available [](here)(https://fivethirtyeight.com/features/the-worlds-favorite-donald-trump-tweets/).
#' 
#' Load required packages to reproduce analysis.  
#' 
## ---- message=FALSE, warning=FALSE---------------------------------------
library(fivethirtyeight)
library(ggplot2)
library(dplyr)
library(readr)
library(tidytext)
library(textdata)
library(stringr)
library(lubridate)
library(knitr)
library(hunspell)
# Turn off scientific notation
options(scipen = 99)

#' ## Check date range of tweets
#' 
## ----date_range----------------------------------------------------------
## check out structure and date range ------------------------------------------------
(minDate <- min(date(trump_twitter$created_at)))
(maxDate <- max(date(trump_twitter$created_at)))

#' 
#' 
#' # Create vectorised stemming function using hunspell
## ----hunspell------------------------------------------------------------
my_hunspell_stem <- function(token) {
  stem_token <- hunspell_stem(token)[]([](1))
  if (length(stem_token) == 0) return(token) else return(stem_token[](1))
}
vec_hunspell_stem <- Vectorize(my_hunspell_stem, "token")

#' 
#' 
#' # Clean text by tokenizing & removing urls/stopwords 
#' We first remove URLs and stopwords as specified in the `tidytext` library.  Stopwords are common words in English.  We also do spellchecking using hunspell.
## ----tokens--------------------------------------------------------------
trump_tokens <- trump_twitter %>% 
  mutate(text = str_replace_all(text, 
                                pattern=regex("(www|https?[](^\\s)+)"), 
                                replacement = "")) %>% #rm urls
  mutate(text = str_replace_all(text,
                                pattern = "[]([](:digit:))",
                                replacement = "")) %>% 
  unnest_tokens(tokens, text) %>% #tokenize
  mutate(tokens = vec_hunspell_stem(tokens)) %>% 
  filter(!(tokens %in% stop_words$word)) #rm stopwords

#' 
#' 
#' # Sentiment analysis
#' To measure the sentiment of tweets, we used the AFINN lexicon for each (non-stop) word in a tweet. The score runs between -5 and 5.  We then sum the scores for each word across all words in one tweet to get a total tweet sentiment score. 
## ----sentiment-----------------------------------------------------------
afinn_sentiment <- system.file("extdata", "afinn.csv", package = "fivethirtyeight") %>% 
  read_csv()
trump_sentiment <- trump_tokens %>% 
  inner_join(afinn_sentiment, by=c("tokens"="word")) 

trump_full_text_sent <- trump_sentiment %>% 
  group_by(id) %>% 
  summarise(score = sum(value, na.rm=TRUE)) %>% 
  ungroup() %>% 
  right_join(trump_twitter, by="id") %>% 
  mutate(score_factor = ifelse(is.na(score), "Missing score", 
                               ifelse(score < 0, "-.Negative", 
                                      ifelse(score == 0, "0", "+.Pos"))))

#' 
#' ## Distribution of sentiment scores
#' 
## ------------------------------------------------------------------------
trump_full_text_sent %>%
  count(score_factor) %>% mutate(prop = prop.table(n))

#' 
#' 46.4% of tweets did not have sentiment scores.  15.4% were net negative and 36.6% were net positive.
#' 
## ----sentiment_hist, fig.width=7, , warning=FALSE------------------------
ggplot(data=trump_full_text_sent, aes(score)) + 
  geom_histogram(bins = 10)

#' 
#' 
#' 
#' # plot sentiment over time
## ----plot_time, fig.width=7----------------------------------------------
sentOverTimeGraph <- ggplot(data=filter(trump_full_text_sent,!is.na(score)), aes(x=created_at, y=score)) +
  geom_line() + 
  geom_point() +
  xlab("Date") +
  ylab("Sentiment (afinn)") +
  ggtitle(paste0("Trump Tweet Sentiment (",minDate," to ",maxDate,")"))
sentOverTimeGraph

#' 
#' 
#' # Examine top 5 most positive tweets
## ----pos_tweets----------------------------------------------------------
most_pos_trump <- trump_full_text_sent %>% 
  arrange(desc(score)) %>% 
  head(n=5) %>% 
  .[]([]("text"))

kable(most_pos_trump, format="html")

#' 
#' # Examine top 5 most negative tweets
## ---- neg_tweets---------------------------------------------------------
most_neg_trump <- trump_full_text_sent %>% 
  arrange(score) %>% 
  head(n=5) %>% 
  .[]([]("text"))
kable(most_neg_trump, format = "html")

#' 
#' 
#' 
#' # When is trumps favorite time to tweet?
#' Total number of tweets and average sentiment (when available) by hour of the day, day of the week, and month
## ----tweet_time----------------------------------------------------------
trump_tweet_times <- trump_full_text_sent %>% 
  mutate(weekday = wday(created_at, label=TRUE),
         month   = month(created_at, label=TRUE),
         hour    = hour(created_at),
         month_over_time = round_date(created_at,"month"))

plotSentByTime <- function(trump_tweet_times, timeGroupVar) {
  timeVar <- substitute(timeGroupVar)
  timeVarLabel <- str_to_title(timeVar)
  
  trump_tweet_time_sent <- trump_tweet_times %>% 
    rename(timeGroup = !! timeVar) %>% 
    group_by(timeGroup) %>% 
    summarise(score = mean(score, na.rm=TRUE), Count = n()) %>% 
    ungroup()

  ggplot(trump_tweet_time_sent, aes(x=timeGroup, y=Count, fill = score)) +
    geom_bar(stat="identity") +
    xlab(timeVarLabel) +
    ggtitle(paste("Trump Tweet Count & Sentiment by", timeVarLabel))
}

#' 
#' 
## ----plot_hour, fig.width=7, warning=FALSE-------------------------------
plotSentByTime(trump_tweet_times, "hour")

#' 
#' * Trump tweets the least between 4 and 10 am. 
#' * Trump's tweets are most positive during the 10am hour. 
#' 
#' 
## ----plot_weekday, fig.width=7, warning=FALSE----------------------------
plotSentByTime(trump_tweet_times, "weekday")

#' 
#' * Trump tweeted the most on Tuesday and Wednesday 
#' * Trump was most positive in the second part of the work week (Wed, Thurs, Fri)
#' 
## ----plot_month, fig.width=7, warning=FALSE------------------------------
plotSentByTime(trump_tweet_times, "month_over_time")

#' 
#' * In this dataset, the number of tweets decreased after November 2015 and drastically dropped off after March 2016.  It is unclear if this is a result of actual decrease in tweeting frequency or a result of the data collection process.
