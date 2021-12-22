from collections import defaultdict

from predict import Predictor
import pandas as pd
import numpy as np
from loaddata import Data_Reader
from IPython import embed

import baostock as bs
import numpy as np


def download_data(code, main):
    """
    :param code: type:str   ex:sh.600000
    :return: type:list
    """
    if main:
        rs_result = bs.query_history_k_data_plus(code, "date,close,volume", start_date='2017-01-01',
                                                 end_date='2021-12-2', frequency="d", adjustflag="3")
    else:
        rs_result = bs.query_history_k_data_plus(code, "date,close", start_date='2017-01-01', end_date='2021-12-2',
                                                 frequency="d", adjustflag="3")
    df_result = rs_result.get_data()
    return df_result


df = pd.read_csv("data.csv")
res = pd.read_csv("causality.csv")
pdt = Predictor(df, res)

prediction = defaultdict(list)
stocks = pdt.stocks_to_predict()

for compares, (lags, _) in stocks.items():
    #print(compares)
    n2, n1 = map(int, compares.split(","))
    prediction["stock" + str(n2)].append(n1)
print(prediction)

reader = Data_Reader()
reader.read_data()
stock_list = reader.code_list
res_list = []
for compares, (lags, _) in stocks.items():
    n2, n1 = map(int, compares.split(","))
    print("current mainstock is : ", "stock" + str(n2), "code is ", stock_list[n2 - 1])
    mainstock = stock_list[n2 - 1]
    for n1 in prediction["stock" + str(n2)]:
        print("adding", n1)
        res_list.append(stock_list[n1 - 1])
    print(res_list)

    output_list = []
    lg = bs.login()
    m = download_data(mainstock, True)
    close = list(map(float, list(m["close"])))
    volume = list(map(float, list(m["volume"])))
    output_list.append(close)
    output_list.append(volume)
    for j in res_list:
        n = download_data(j, False)
        # print(len(m), len(n))
        # embed()
        if len(n) == len(m):
            close = list(map(float, list(n["close"])))
            output_list.append(close)
            print(j, "added")
    bs.logout()

    for i in range(len(output_list)):
        mean = sum(output_list[i]) / len(output_list[i])
        for j in range(len(output_list[i])):
            output_list[i][j] = output_list[i][j] / mean
    # 做差分
    for i in range(len(output_list)):
        for j in range(len(output_list[i]) - 1):
            output_list[i][j] = output_list[i][j + 1] - output_list[i][j]
        output_list[i].pop(-1)

    data = pd.DataFrame(
        {"close": output_list[0], "volume": output_list[1]})
    for i in range(2, len(output_list)):
        data["stock"+str(i)] = output_list[i]
    data.to_csv("grangerdata.csv", index=False)
    break
