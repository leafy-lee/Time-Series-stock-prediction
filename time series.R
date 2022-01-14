library(zoo)
library(tseries)
library(forecast)
library(TSA)
library(parallel)
library(rugarch)
setwd("C:/Users/liyif/PycharmProjects/pythonProject1")
data<-read.csv("sh.601318.csv")
data
spec <- ugarchspec(variance.model = list(model = "sGARCH", 
                                         garchOrder = c(4, 5), 
                                         submodel = NULL, 
                                         external.regressors = NULL, 
                                         variance.targeting = FALSE), 
                   
                   mean.model     = list(armaOrder = c(1, 1), 
                                         external.regressors = NULL, 
                                         distribution.model = "norm", 
                                         start.pars = list(), 
                                         fixed.pars = list()))

garch <- ugarchfit(spec = spec, data = diff1, solver.control = list(trace=0))
res = c(-3.1,-0.8, 1.2,0.6,2.8,-0.9,0.3,-1.4,-2.5,-1.1,0.9,1.4)
arr=arima(res, order=c(2,0,0),method = "ML",fixed=c(0.9,0.09,0))
arr.sim()
arr1 = rima(res, order=c(0,1,1),method = "ML",fixed=c(-0.1,0))
arr
data<-read.csv("sh601318.csv")
data
close=ts(data[,2])
close
plot(close)
#闈炲钩绋? 涓�闃跺樊鍒?

diff1=diff(close)


plot(diff1)
eacf(diff1)
Box.test(close)
adf.test(close)
adf.test(diff1)
#diff1 p-0.01 alternative hypothesis: stationary 璁や负宸垎鍚庡簭鍒楀钩绋?
Box.test(close,type='Ljung')
acf=acf(diff1,lag=80)
acf
pacf=pacf(diff1,lag=80)
pacf

Box.test(diff1,lag=6)
Box.test(diff1,lag=12)
#宸垎搴忓垪涓虹櫧鍣０搴忓垪鍙兘鎬т笉澶?
auto.arima(diff1,ic='aic',trace=TRUE)

AIC(arima(diff1,order=c(0,0,0),method='ML'))
AIC(arima(diff1,order=c(1,0,1),method='ML'))
AIC(arima(diff1,order=c(2,0,1),method='ML'))
AIC(arima(diff1,order=c(1,0,2),method='ML'))
AIC(arima(diff1,order=c(2,0,2),method='ML'))
AIC(arima(diff1,order=c(3,0,2),method='ML'))
AIC(arima(diff1,order=c(3,0,2),method='ML'))
AIC(arima(diff1,order=c(2,0,3),method='ML'))
AIC(arima(diff1,order=c(3,0,3),method='ML'))
AIC(arima(diff1,order=c(3,0,4),method='ML'))
AIC(arima(diff1,order=c(4,0,3),method='ML'))
AIC(arima(diff1,order=c(4,0,4),method='ML'))
AIC(arima(diff1,order=c(4,0,5),method='ML'))
AIC(arima(diff1,order=c(5,0,4),method='ML'))


result=arima(diff1,order=c(4,0,5))
result
plot(result)
abline(h=0)
plot(residuals(result))
qqnorm(residuals(result))
qqline(residuals(result))
shapiro.test(residuals(result))

acf(residuals(result))
pacf(residuals(result))
Box.test(residuals(result),type='Ljung')


arima1=arima(close,order=c(4,1,5))
arima1
fore=predict(arima1,n.ahead=20)
fore$pred
ts.plot(close,fore$pred,col=1:2)
#lines(fore$pred,type="p",col=2)
lines(fore$pred+fore$se,lty="dashed",col=4)
lines(fore$pred-fore$se,lty="dashed",col=4)





yy=c(8.7,9.6,6.1,8.4,6.8,5.5,7.1,8.0,6.6,7.9,7.6,7.8,9.0,7.0,6.3)
xx=c(9.1,8.3,7.2,7.5,6.3,5.8,7.6,8.1,7.0,7.3,6.5,6.9,8.2,6.8,5.5)

cyx=coef(lm(yy~xx))

md=median(xx)
xx1=xx[xx<=md]
xx2=xx[xx>md]
yy1=yy[xx<md]
yy2=yy[xx>md]
md1=median(xx1)
md2=median(xx2)
mw1=median(yy1)
mw2=median(yy2)
beta=(mw2-mw1)/(md2-md1)
alpha=median(yy-beta*xx)
plot(xx,yy)
abline(alpha,beta)
abline(c(cyx),lty=2)

alpha=0
beta=0

y=c(76,103,69,50,86,85,74,58,62,88,210)
x=c(33,45,30,20,39,34,34,21,27,38,30)
r=rle(x)
if(length(r$lengths)==length(x))    #不打结
{y=y}
if(length(r$lengths)<length(x))    #打结
{
  m=r$lengths>1
  t1=which(m==1)
  for(i in 1:length(t1))
  {
    n=r$values[t1[i]]
    t3=which(x==n)          #确定结点位置 
    x=c(x[-t3],n)  
    y=c(y[-t3],median(y[t3]))     #替换原y值
  }
}
k=c(1:length(x))
a=(y[k>1]-y[1])/(x[k>1]-x[1]) 
for(i in 2:(length(x)-1))
{
  b=(y[k>i]-y[i])/(x[k>i]-x[i])  #任意两点斜率
  a=c(a,b)
}
beta=a
beta.e=median(beta)             #斜率估计值
alpha=y-beta.e*x
alpha.e=median(alpha)           #截距估计值
beta.e
alpha.e
plot(x,y)
abline(alpha.e,beta.e)




library(TSA);library(locfit);library(mgcv)
data(veilleux)
predator=veilleux[,1]
plot(predator,lty=2,type="b",xlab="时间",ylab="毛虫")
predator.eq = window(predator,start=c(7,1))
lines(predator.eq)
Keenan.test(log(predator.eq),4)
Tsay.test(log(predator.eq),4)
for(i in 1:4)print(tlrt(log(predator.eq),4,d=i,a=0.25,b=0.75))
AICM=NULL
for(d in 1:4){predator.tar=tar(y=log(predator.eq),p1=4,p2=4,d=d,a=0.1,b=0.9)
AICM=rbind(AICM,c(d,predator.tar$AIC,signif(predator.tar$thd,4)))}
AICM
predator.tar.1=tar(y=log(predator.eq),p1=4,p2=4,d=2,a=0.1,b=0.9,print=T)
tar(y=log(predator.eq),p1=4,p2=4,d=2,a=0.1,b=0.9,print=T,method="CLS")
predator.tar.2=tar(y=log(predator.eq),p1=4,p2=4,d=3,a=0.1,b=0.9,print=T)

set.seed(356813)
plot(tar.sim(n=57,object=predator.tar.1)$y,ylab=expression(X[t]),xlab=expression(t),type="o")
plot(tar.sim(n=57,object=predator.tar.2)$y,ylab=expression(X[t]),xlab=expression(t),type="o")





