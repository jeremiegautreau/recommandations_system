# Benchmark in R language of a recommandations system

library(tidyverse)
library(data.table)
library(dplyr)
library(reshape2)
library(matrixStats)
library(pracma)
library(irlba)
library(proxy)
library(lsa)

# Importation of datasets

ratings <- read_csv("C:/lamp/htdocs/MEDAS/ratings.csv")
View(ratings)

movie <- read_csv("C:/lamp/htdocs/MEDAS/movies.csv")
View(movie)

tbl1 <- merge(ratings, movie, by = "movieId", all = TRUE)
View(tbl1)

# filtering movies under 100 ratings

nb_ratings <- tbl1 %>%
  dcast(movieId ~ ., value.var = "rating", fun.aggregate = length, fill = 0) %>%
  rename("rating" = ".") %>%
  filter(rating > 100)
View(nb_ratings)


tbl2 <- tbl1 %>%
  filter(movieId %in% nb_ratings$movieId)
View(tbl2)

# Creation of item based matrix

matrix <- tbl2 %>%
  dcast(title ~ userId, value.var = "rating", fill = NA) %>%
  column_to_rownames("title")
View(matrix)

# Normalization

matrix_norm <- matrix - rowMeans(matrix, na.rm = TRUE)

# Creating similiraty matrix with pearson correlation

movie_corr <- cor(t(matrix_norm),
  use = "pairwise.complete.obs",
  method = "pearson"
)

# Creating similarity matrix with cosine

movie_cos <- replace(matrix_norm, is.na(matrix_norm), 0)
movie_cos <- cosine(t(movie_cos))
movie_cos <- as.data.frame(movie_cos)

# Example for 1 user and 1 movie

user <- "1"
movie <- "Aladdin (1992)"

watched_movie <- data.frame(title = rownames(matrix_norm),
                            rating = matrix_norm[, user]) %>%
  filter(!is.na(rating)) %>%
  arrange(desc(rating))

movie_sim <- data.frame(title = rownames(matrix_norm),
                        similarity_score = movie_cos[, movie]) %>%
  arrange(desc(similarity_score))

n <- 5

sim_u_m <- watched_movie %>%
  left_join(movie_sim, by = "title") %>%
  top_n(n, similarity_score)

predicted_rating <- round(weighted.mean(sim_u_m$rating,
    sim_u_m$similarity_score
  ),
  6
)

cat(paste("the predicted rating for", movie, "is", predicted_rating, "\n"))


# Creation of the item based recommandations function

recommendation_item <- function(user, nb_item, nb_reco, matrix, matrix_norm) {
  unwatched_movie <- data.frame(title = rownames(matrix_norm),
                                pred_rating = matrix_norm[, user]) %>%
    filter(is.na(pred_rating))

    watched_movie <- data.frame(title = rownames(matrix_norm),
                                rating = matrix_norm[, user]) %>%
      filter(!is.na(rating)) %>%
      arrange(desc(rating))

  for (movie in unwatched_movie$title) {
    movie_sim <- data.frame(title = rownames(matrix_norm),
                            similarity_score = matrix[movie, ])

    movie_pred <- watched_movie %>%
      inner_join(movie_sim, by = "title") %>%
      slice(1:nb_item)

    unwatched_movie[unwatched_movie$title == movie, "pred_rating"] <- round(
      weighted.mean(movie_pred$rating, movie_pred$similarity_score),
      6
    )
  }

  reco <- unwatched_movie %>%
    arrange(desc(pred_rating)) %>%
    slice(1:nb_reco)

  return(reco)
}

# test of the recommandations function

user <- 6
nb_item <- 5
nb_reco <- 6
matrix <- movie_cos


recommendation_item(user, nb_item, nb_reco, matrix, matrix_norm)


user <- 6
nb_item <- 5
nb_reco <- 6
matrix <- movie_corr


recommendation_item(user, nb_item, nb_reco, matrix, matrix_norm)
