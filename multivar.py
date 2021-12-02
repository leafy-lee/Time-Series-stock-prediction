import matplotlib.pyplot as plt
from statsmodels.tsa.vector_ar.var_model import VAR
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
import warnings

warnings.filterwarnings("ignore")


def getparams(stock_list, lags, df_difference):
    # input stocklist=['stock1','stock3','stock6','stock14','stock26']
    # 要预测内容放在第一
    df_difference = df_difference[stock_list]
    model = VAR(df_difference)
    # print(model)
    model_fitted = model.fit(lags)
    return list(model_fitted.params[stock_list[0]])


# print(get_params(['stock1','stock3','stock6','stock14','stock26'],2,df_difference))

def predict(stock_list, lags, df_difference, predict_start):
    # predictstart 为当天数据已知，预测下一天，为保证list index in range >10
    # ex list[start-1]为已知数据 目标为list[start]
    # 最大上限为699

    coef = getparams(stock_list, lags, df_difference[:600])
    l1 = np.array(df_difference[stock_list])
    l2 = l1.tolist()
    # print(len(l2))
    ans = coef[0]
    # print(len(coef))
    # print(coef)
    for i in range(lags):
        for j in range(len(stock_list)):
            # print(l2[predictstart-1-i][j],coef[i*lags+j+1])
            # print(predictstart-1-i,j,i*len(stocklist)+j+1)
            ans += l2[predict_start - 1 - i][j] * coef[i * len(stock_list) + j + 1]
    return ans


# print(predict(['stock1','stock3','stock6','stock14','stock26'],1,df_difference,698))

def True_or_False(stock_list, lags, df_difference):
    l1 = np.array(df_difference[stock_list])
    right = 0
    wrong = 0
    for i in range(100, 699):
        if predict(stock_list, lags, df_difference, i) * l1[i][0] > 0:
            right += 1
        elif predict(stock_list, lags, df_difference, i) * l1[i][0] < 0:
            wrong += 1
    return [right, wrong]


# print(True_or_False(['stock1','stock3','stock6','stock14','stock26'],1,df_difference))

def linear_test(stock_list, lags, df_difference, verbose=False):
    print("predicting from list", stock_list)
    if verbose:
        print("while df_diff is ", df_difference)
    l1 = np.array(df_difference[stock_list])
    x = []
    y = []
    for i in range(600, 699):
        x.append(predict(stock_list, lags, df_difference, i))
        y.append(l1[i][0])
    if verbose:
        plt.scatter(x, y, s=50, c='b', alpha=0.5)
        plt.show()
    x = sm.add_constant(x)  # 若模型中有截距，必须有这一步
    model = sm.OLS(y, x).fit()  # 构建最小二乘模型并拟合
    # print(model.summary()) # 输出回归结果
    if verbose:
        print(model.summary())
    print(model.rsquared)
    return model.rsquared


if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    ddf_difference = df.diff().dropna()
    '''
    for stock in range(28):
        linear_test( ['stock'+str(stock+1)]+['stock'+str(i+1) if i<stock else 'stock'+str(i+2) for i in range(27)], 1, ddf_difference)
    '''
    linear_test(['stock10', 'stock6', 'stock14', 'stock18', 'stock19', 'stock28'], 20, ddf_difference)
# print(True_or_False(['stock1','stock3','stock6','stock14','stock26'],2,df_difference))

# linear_test(['stock2','stock7'],20,df_difference)
