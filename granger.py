import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests


def granger_test(df, path="causality.csv"):
    df_transformed = df.diff().dropna()
    data = pd.DataFrame({})

    for id in range(27):
        for jd in range(id + 1, 28):
            i = id + 1
            j = jd + 1
            result = grangercausalitytests(df_transformed[["stock" + str(i), "stock" + str(j)]], maxlag=5, verbose=False)
            lis = []
            for idx in result:
                lis.append(result[idx][0]['ssr_ftest'][1])
            data[str(i) + ", " + str(j)] = lis
            result = grangercausalitytests(df_transformed[["stock" + str(j), "stock" + str(i)]], maxlag=5, verbose=False)
            lis = []
            for idx in result:
                lis.append(result[idx][0]['ssr_ftest'][1])
            data[str(j) + ", " + str(i)] = lis
    data.to_csv(path, index=False)
    return data


if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    granger_test(df)