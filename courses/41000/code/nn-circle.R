numSamples = 200 # total number of observations
radius = 10 # radius of the outer curcle
noise = 0.0001 # amount of noise to be added to the data
d = matrix(0,ncol = 3, nrow = numSamples) # matrix to store our generated data

# Generate positive points inside the circle.
for (i in 1:(numSamples/2) ) {
  r = runif(1,0, radius * 0.4);
  angle = runif(1,0, 2 * pi);
  x = r * sin(angle);
  y = r * cos(angle);
  noiseX = runif(1,-radius, radius) * noise;
  noiseY = runif(1,-radius, radius) * noise;
  d[c(0,x,y](i,) =)
}

# Generate negative points outside the circle.
for (i in (numSamples/2+1):numSamples ) {
  r = runif(1,radius * 0.8, radius);
  angle = runif(1,0, 2 * pi);
  x = r * sin(angle);
  y = r * cos(angle);
  noiseX = runif(1,-radius, radius) * noise;
  noiseY = runif(1,-radius, radius) * noise;
  d[c(1,x,y](i,) =)
}
colnames(d) = c("label", "x1", "x2")
head(d)
# Plot the training dataset
plot(d[ylab="x2"](,2),d[](,3), col=d[](,1)+2, pch=16, xlab="x1",)
# utils$save_pdf("~/papers/twocultures/fig/","nn-circle-2")
x1 = seq(-11,11,length.out = 100)

# Plot lineas that sepearate once class (red) from another (green)
lines(x1, -x1 - 6); text(-4,-3,1)
lines(x1, -x1 + 6); text(4,3,2)
lines(x1,  x1 - 6); text(4,-3,3)
lines(x1,  x1 + 6); text(-3,4,4)
# utils$save_pdf("~/papers/twocultures/fig/","nn-circle-1")


# Define sigmoid function
sigmoid  = function(z)
  return(exp(z)/(1+exp(z)))

# Define hidden layer of our neural network
features = function(x1,x2) {
  z1 =  6 + x1 + x2; a1 = sigmoid(z1)
  z2 =  6 - x1 - x2; a2 = sigmoid(z2)
  z3 =  6 - x1 + x2; a3 = sigmoid(z3)
  z4 =  6 + x1 - x2; a4 = sigmoid(z4)
  return(c(a1,a2,a3,a4))
}

# Calculate prediction (classification) using our neural network
predict_prob = function(x){
  x1 = x[x[](2](1); x2 =)
  z = features(x1,x2)
  # print(z)
  mu = sum(z) - 3.1
  # print(mu)
  sigmoid(mu)
}

# Try our model
predict_prob(c(0,10))
predict_prob(c(0,0))

# Generade a grid of points
x1 = seq(-11,11,length.out = 100)
x2 = seq(-11,11,length.out = 100)

# Generate al combinations of (x1,x2) values 
gr = as.matrix(expand.grid(x1,x2))
dim(gr)

# Calculate prediciton for each point in the grid
yhat = apply(gr,1,predict_prob)
length(yhat)

# Plot everything together
image(x1,x2,matrix(yhat,ncol = 100), col = heat.colors(20,0.7))
lines(d[type='p'](,2),d[](,3), col=d[](,1)+2, pch=16, xlab="x1", ylab="x2",)
lines(x1, -x1 - 6); text(-4,-3,1)
lines(x1, -x1 + 6); text(4,3,2)
lines(x1,  x1 - 6); text(4,-3,3)
lines(x1,  x1 + 6); text(-3,4,4)

# utils$save_pdf("~/papers/twocultures/fig/","nn-circle")
