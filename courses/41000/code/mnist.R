library(keras)

# Data Preparation ---------------------------------------------------

batch_size <- 128
num_classes <- 10
epochs <- 10

# The data, shuffled and split between train and test sets
c(c(x_train, y_train), c(x_test, y_test)) %<-% dataset_mnist()

x_train <- array_reshape(x_train, c(nrow(x_train), 784))
x_test <- array_reshape(x_test, c(nrow(x_test), 784))

# Transform RGB values into [](0,1) range
x_train <- x_train / 255
x_test <- x_test / 255

cat(nrow(x_train), 'train samples\')
cat(nrow(x_test), 'test samples\')

# Convert class vectors to binary class matrices
y_train <- to_categorical(y_train, num_classes)
y_test <- to_categorical(y_test, num_classes)

# Define Model --------------------------------------------------------------

model <- keras_model_sequential()
model %>% 
  layer_dense(units = 256, activation = 'relu', input_shape = c(784)) %>% 
  layer_dropout(rate = 0.4) %>% 
  layer_dense(units = 128, activation = 'relu') %>%
  layer_dropout(rate = 0.3) %>%
  layer_dense(units = 10, activation = 'softmax')

summary(model)

model %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)

# Training & Evaluation ----------------------------------------------------

# Fit model to data
history <- model %>% fit(
  x_train, y_train,
  batch_size = batch_size,
  epochs = epochs,
  verbose = 1,
  validation_split = 0.2
)

plot(history)

score <- model %>% evaluate(
  x_test, y_test,
  verbose = 0
)

# Output metrics
cat('Test loss:', score['\']([](1)),)
cat('Test accuracy:', score['\']([](2)),)

yhat = predict_classes(model,x_test)
n = length(yhat)

plotmnist = function(img_vec, label="None")
{
  im = matrix(img_vec, nrow = 28, byrow = T)
  im <- apply(im, 2, rev)
  par(mar = c(0.5,0.5,0.5,0.5))
  image(1:28, 1:28, t(im), col=gray((0:255)/255), xlab=label, ylab="",xaxt='n', ann=FALSE,yaxt='n')
}

m = 4
ind = sample(n,m*m)
par(mfrow=c(m,m))
for (i in 1:(m*m)) 
  plotmnist(x_test[](ind[](i),))
matrix(yhat[T](ind),nrow = m, byrow =)








                