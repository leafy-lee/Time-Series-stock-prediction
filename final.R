
setwd("C:/R")
library(rugarch)
library(zoo)
library(tseries)
library(forecast)
library(quantmod)
library(lubridate)
library(tidyverse)
library(fGarch, quietly = TRUE)
data<-read.csv("sh601318.csv")
data
close=ts(data[,2])

#观察是否需要差分
plot(close)
plot(log(close))

diff1=diff(close)
plot(diff1)

acf(diff1)
pacf(diff1)
AIC(arima(diff1,order=c(0,0,0),method='ML'))
AIC(arima(diff1,order=c(1,0,0),method='ML'))
AIC(arima(diff1,order=c(2,0,0),method='ML'))
AIC(arima(diff1,order=c(3,0,0),method='ML'))
AIC(arima(diff1,order=c(4,0,0),method='ML'))
AIC(arima(diff1,order=c(5,0,0),method='ML'))
AIC(arima(diff1,order=c(6,0,0),method='ML'))
AIC(arima(diff1,order=c(7,0,0),method='ML'))
AIC(arima(diff1,order=c(8,0,0),method='ML'))
AIC(arima(diff1,order=c(9,0,0),method='ML'))
AIC(arima(diff1,order=c(10,0,0),method='ML'))
AIC(arima(diff1,order=c(11,0,0),method='ML'))

result=arima(diff1,order=c(3,0,4))
result
plot(result)
plot(residuals(result))
qqnorm(residuals(result))
qqline(residuals(result))
shapiro.test(residuals(result))

result1=arima(diff1,order=c(6,0,0))
result1
plot(result1)
plot(residuals(result1))
qqnorm(residuals(result1))
qqline(residuals(result1))
shapiro.test(residuals(result1))

oil.mod2<-garchFit(~arma(3,4)+garch(0,1),data=diff1)
x=ts(oil.mod2@fitted[500:600]+close[500:600])
y=ts(diff1[500:600]+close[500:600])
ts.plot(x,y,gpars=list(col=c("blue","red")))
plot(oil.mod6, which=13)
plot(oil.mod6, which=9)

oil.mod6<-garchFit(~arma(3,4)+garch(1,1),data=diff1)
x=ts(oil.mod6@fitted[500:600]+close[500:600])
y=ts(diff1[500:600]+close[500:600])
ts.plot(x,y,gpars=list(col=c("blue","red")))
plot(oil.mod6, which=13)
plot(oil.mod6, which=9)

oil.mod1<-garchFit(~arma(3,4)+garch(1,1),data=diff1,cond.dist="sstd")
a=500
b=600
x1=ts(oil.mod1@fitted[a:b]+close[a:b])
y1=ts(diff1[a:b]+close[a:b])
ts.plot(x1,y1,gpars=list(col=c("blue","red")))
plot(oil.mod1, which=13)

plot(oil.mod1, which=9)

