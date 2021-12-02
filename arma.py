# -*- coding: utf-8 -*-
import statsmodels.tsa.ar_model as sta
from statsmodels.tsa.arima.model import ARIMA
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox as lb_test
import matplotlib.pyplot as plt
import baostock as bs
import pandas as pd
import numpy as np
from IPython import embed
'''
#### 登陆系统 ####
lg = bs.login()
#### 获取沪深A股历史K线数据 ####
rs_result = bs.query_history_k_data_plus("sz.002739", "date,code,open,high,low,close,preclose,pctChg,volume",
                                         start_date='2019-01-01', end_date='2021-11-26', frequency="d", adjustflag="3")
df_result = rs_result.get_data()
#### 登出系统 ####
bs.logout()
result0=np.array(df_result)
data_list =result0.tolist()
# print(type(df_result))
df_new = pd.DataFrame(df_result, columns=['date', 'close'])
# print(df_new)
df_new.to_csv("sz002739.csv", index=False, sep=',')
'''
df = pd.read_csv('sz002739.csv', encoding='utf-8', index_col='date')
df.plot()
plt.show()
# embed()
# print(df)

diff = df.diff(1).dropna()
# statsmodels.graphics.tsaplots.plot_acf(diff)
# statsmodels.graphics.tsaplots.plot_pacf(diff)
print(lb_test(diff))
diff.plot()
plt.show()



'''
temp = diff
model = sta.AutoReg(temp, lags=5)
results_AR = model.fit()
plt.figure(figsize=(10, 4))
plt.plot(temp, 'b', label='diff')
plt.plot(results_AR.fittedvalues, 'r', label='AR model')
plt.legend()

# AR(p)模型阶数
print("AR(p)模型阶数")
print(len(results_AR.roots))

# 以上模型平稳性检验
pi, sin, cos = np.pi, np.sin, np.cos
r1 = 1
theta = np.linspace(0, 2 * pi, 360)
x1 = r1 * cos(theta)
y1 = r1 * sin(theta)
plt.figure(figsize=(6, 6))
plt.plot(x1, y1, 'k')  # 画单位圆
roots = 1 / results_AR.roots  # 注意，这里results_AR.roots 是计算的特征方程的解，特征根应该取倒数
for i in range(len(roots)):
    plt.plot(roots[i].real, roots[i].imag, '.r', markersize=8)  # 画特征根
plt.show()
'''

temp = diff
# 定阶方法
fig = plt.figure(figsize=(20, 5))
ax1 = fig.add_subplot(111)
# fig = sm.graphics.tsa.plot_pacf(temp, ax=ax1)

# embed()
'''
# AIC BIC，HQ
for i in range(1, 6):  # 从1阶开始算
    aicList = []
    for j in range(1, 6):
        order = (i, 0, j)  # 这里使用了ARIMA模型，order 代表了模型的(p,q)值，我们令q始终为0，就只考虑了AR情况。
        tempModel = ARIMA(temp, order=order).fit()
        aicList.append(tempModel.aic)
    plt.title("arma "+str(i))
    plt.figure(figsize=(6, 6))
    plt.plot(aicList, 'r', label='aic value')
    plt.legend(loc=0)
plt.show()
'''
temp = df[:700]
model = ARIMA(df, order=(4, 1, 2)).fit()
'''
fore = []
cur = []
for i in range(5):
    new = model.apply(df[:600+i])
    fore.append(list(new.forecast(1))[0])
    embed()
'''
plt.figure(figsize=(10, 4))
plt.plot(df[1:], 'b', label='close')
plt.plot(list(model.fittedvalues[1:]), 'r', label='ARIMA 412 model')
plt.legend()
plt.show()


embed()