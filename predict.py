from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
from statsmodels.tsa.vector_ar.var_model import VAR
from multivar import linear_test, predict
import warnings

warnings.filterwarnings("ignore")

class Predictor():
    """
    predictor for granger prediction
    if granger(a, b)<0.05
    predict(b, a)-->predict value of a
    """

    def __init__(self, data, granger_res):
        self.data = data
        self.diff = data.diff().dropna()
        self.causality = granger_res

    def stocks_to_predict(self):
        stocks = {}
        for compares in self.causality:
            for lags, causality in enumerate(self.causality[compares]):
                # print(compares, lags+1, causality)
                if causality < 0.05:
                    # print("stocks affected found", compares, lags)
                    if compares in stocks:
                        # print("same compares, ori causality and lags and new causality and lags is %f, %d and %f, %d"%(stocks[compares][1], stocks[compares][0], causality, lags))
                        if causality < stocks[compares][1]:
                            # print("changed")
                            stocks[compares] = (lags+1, causality)
                    else:
                        stocks[compares] = (lags+1, causality)
        return stocks

    def auto_predict(self):
        stocks = self.stocks_to_predict()
        pred = defaultdict(list)
        for compares, (lags, _) in stocks.items():
            n2, n1 = map(int, compares.split(","))
            ans = self.predict_oneday(n1, n2, lags)
            pred[n2].append((n1, lags, ans))
        return pred

    def get_params(self, number1, number2, lags):
        """
        :param number1: stock 1 type:int
        :param number2: stock 2 type:int
        :param lags: lags of VAR type:int
        :return: params of the model type:list
        """
        stocks = ['stock' + str(number1), 'stock' + str(number2)]
        df_difference = self.diff[stocks]
        model = VAR(df_difference)
        model_fitted = model.fit(lags)
        return list(model_fitted.params[stocks[1]])

    def predict_oneday(self, number1, number2, lags):
        """
        :param number1: stock 1 type:int
        :param number2: stock 2 type:int
        :param lags: lags of VAR type:int
        :return: (predicted stock, value) type:tuple
        """
        # embed()
        coef = self.get_params(number1, number2, lags)
        p1 = self.diff['stock' + str(number1)]
        p2 = self.diff['stock' + str(number2)]
        p1 = np.array(p1)
        p2 = np.array(p2)
        ans = coef[0]
        for i in range(lags):
            ans += p1[-1 + i] * coef[i + 1]
        for i in range(lags):
            ans += p2[-1 + i] * coef[i + lags + 1]
        return ans


# print(predict_oneday(25,21,1,df_difference))
if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    ddf_difference = df.diff().dropna()
    res = pd.read_csv("causality.csv")
    gt = df.diff()[-1:]
    datas = df[:-1]
    pdt = Predictor(datas, res)
    # embed()
    # ans = pdt.predict_oneday(15, 9, 1)
    # print("prediction of stock", 23, "is", ans)
    '''
    prediction = pdt.auto_predict()
    for stock in prediction:
        print("prediction of %d" % stock)
        absmax = 0
        ave = 0
        for influence in prediction[stock]:
            print("\t from %d with lags %d is %lf" % influence)
            ave += influence[2]
            if abs(influence[2]) > abs(absmax):
                absmax = influence[2]
        ave /= len(prediction[stock])
        print("the bravest prediction is ", absmax)
        print("average prediction is", ave)
        print("the ground truth is ", list(gt["stock"+str(stock)])[0])
    '''
    prediction = defaultdict(list)
    stocks = pdt.stocks_to_predict()
    '''
    for compares, (lags, _) in stocks.items():
        n2, n1 = map(int, compares.split(","))
        prediction["stock"+str(n2)].append("stock"+str(n1))
    for stock in prediction:
        linear_test([stock]+prediction[stock], 2, ddf_difference, verbose=False)
    '''
    print(predict(['stock28', 'stock2', 'stock6', 'stock7', 'stock14', 'stock16', 'stock19'], 2, ddf_difference, len(ddf_difference)-3), len(ddf_difference)-1)