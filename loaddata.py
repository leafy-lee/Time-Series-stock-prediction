import baostock as bs
import pandas as pd
import numpy as np
from IPython import embed


class Data_Reader():
    """
    reading the data from the file
    """

    def __init__(self, file="stock.csv"):
        self.file = file
        self.code_list = []
        self.data = None

    def read_data(self, file="stock.csv"):
        data_list = np.array(pd.read_csv(file, encoding="gbk")).tolist()
        for i in range(len(data_list)):
            self.code_list.append(data_list[i][1])
        for i in range(len(self.code_list)):
            self.code_list[i] = str.lower(self.code_list[i][:2]) + '.' + self.code_list[i][2:]
        # print(self.code_list)

    def download_data(self, code):
        """
        :param code: type:str   ex:sh.600000
        :return: type:list
        """
        rs_result = bs.query_history_k_data_plus(code, "date,close", start_date='2019-01-01', end_date='2021-12-2',
                                                 frequency="d", adjustflag="3")
        df_result = rs_result.get_data()

        data_list = np.array(df_result).tolist()
        return data_list

    def addoutput(self):
        date = [i + 1 for i in range(709)]
        self.data = pd.DataFrame({"dates": date})
        for i in range(len(self.code_list)):
            stocks = self.download_data(self.code_list[i])
            st = [stock[1] for stock in stocks]
            self.data["stock" + str(i+1)] = st
            print("stock", i+1, "added")

    def forward(self):
        self.read_data()
        bs.login()
        self.addoutput()
        self.data.to_csv("data.csv", index=False, sep=",")
        bs.logout()
        return self.data

    def update(self):
        raise NotImplementedError


if __name__ == "__main__":
    reader = Data_Reader()
    data = reader.forward()
