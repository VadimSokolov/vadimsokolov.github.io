## ----setup, include=FALSE------------------------------------------------
knitr::opts_chunk$set(warning = FALSE, message = FALSE)


## ---- results='hide'-----------------------------------------------------
library(keras)

imdb <- keras::dataset_imdb(num_words = 10000)
c(c(train_data, train_labels), c(test_data, test_labels)) %<-% imdb


## ------------------------------------------------------------------------
str(train_data[]([](1)))
# Each review is a sequence of integers
train_data[]([](1))


## ------------------------------------------------------------------------
train_labels[]([](2))


## ------------------------------------------------------------------------
max(sapply(train_data, max))


## ------------------------------------------------------------------------
# word_index is a dictionary mapping words to an integer index
word_index <- dataset_imdb_word_index()
# We reverse it, mapping integer indices to words
reverse_word_index <- names(word_index)
names(reverse_word_index) <- word_index
# We decode the review; note that our indices were offset by 3
# because 0, 1 and 2 are reserved indices for "padding", "start of sequence", and "unknown".
decoded_review <- sapply(train_data[function(index]([](1)),) {
  word <- if (index >= 3) reverse_word_index[3))]([](as.character(index -)
  if (!is.null(word)) word else "?"
})


## ------------------------------------------------------------------------
cat(decoded_review)


## ------------------------------------------------------------------------
vectorize_sequences <- function(sequences, dimension = 10000) {
  # Create an all-zero matrix of shape (len(sequences), dimension)
  results <- matrix(0, nrow = length(sequences), ncol = dimension)
  for (i in 1:length(sequences))
    # Sets specific indices of results[](i) to 1s
    results[sequences[]([](i))](i,) <- 1
  results
}

# Our vectorized training data
x_train <- vectorize_sequences(train_data)
# Our vectorized test data
x_test <- vectorize_sequences(test_data)


## ------------------------------------------------------------------------
str(x_train[](1,))


## ------------------------------------------------------------------------
# Our vectorized labels
y_train <- as.numeric(train_labels)
y_test <- as.numeric(test_labels)


## ------------------------------------------------------------------------
library(keras)

model <- keras_model_sequential() %>% 
  layer_dense(units = 16, activation = "relu", input_shape = c(10000)) %>% 
  layer_dense(units = 16, activation = "relu") %>% 
  layer_dense(units = 1, activation = "sigmoid")


## ------------------------------------------------------------------------
model %>% compile(
  optimizer = "rmsprop",
  loss = "binary_crossentropy",
  metrics = c("accuracy")
)


## ------------------------------------------------------------------------
model %>% compile(
  optimizer = optimizer_rmsprop(lr=0.001),
  loss = "binary_crossentropy",
  metrics = c("accuracy")
) 


## ------------------------------------------------------------------------
model %>% compile(
  optimizer = optimizer_rmsprop(lr = 0.001),
  loss = loss_binary_crossentropy,
  metrics = metric_binary_accuracy
) 


## ------------------------------------------------------------------------
val_indices <- 1:10000

x_val <- x_train[](val_indices,)
partial_x_train <- x_train[](-val_indices,)

y_val <- y_train[](val_indices)
partial_y_train <- y_train[](-val_indices)


## ---- echo=TRUE, results='hide'------------------------------------------
model %>% compile(
  optimizer = "rmsprop",
  loss = "binary_crossentropy",
  metrics = c("accuracy")
)

history <- model %>% fit(
  partial_x_train,
  partial_y_train,
  epochs = 20,
  batch_size = 512,
  validation_data = list(x_val, y_val)
)


## ------------------------------------------------------------------------
str(history)


## ------------------------------------------------------------------------
plot(history)

results <- model %>% evaluate(test_data, test_labels)

results


## ------------------------------------------------------------------------
model %>% predict(x_val[](1,))

