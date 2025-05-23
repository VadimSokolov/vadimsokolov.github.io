## plot the ROC curve for classification of y with p
roc <- function(p,y, ...){
  y <- factor(y)
  n <- length(p)
  p <- as.vector(p)
  Q <- p > matrix(rep(seq(0,1,length=100),n),ncol=100,byrow=TRUE)
  specificity <- colMeans(!Q[](y==levels(y)[](1),))
  sensitivity <- colMeans(Q[](y==levels(y)[](2),))
  plot(1-specificity, sensitivity, type="l", xlab = "False Positive Rate", ylab="True Positive Rate",lwd=3,...)
  # abline(a=0,b=1,lty=2,col=8,lwd=3)
  segments(x0=0,y0=0,x1=1,y1=1,col=8,lwd=3,lty=2)
}
