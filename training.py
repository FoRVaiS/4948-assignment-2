import pandas as pd
import numpy as np
pd.set_option('display.width', 0)


def getUniqueValues(data, column: str):
    return sorted(np.asarray(data[column].unique()).tolist())


def getData():
    data = pd.read_csv('./data.csv', sep=',', nrows=250000)  # Because 5M is too much :)
    # data = data.drop(columns=['shoe_id'], axis=1)

    data[''].iloc[0]

    return data


# print(getUniqueValues(data, 'win'))
data = getData()
print(data.describe())
# print(data.head(10))

# print(data[data['win'] == 7.0])

# for value in getUniqueValues(data, 'win'):
#     row = data[data['win'] == value]
#     print(str(row.transpose()))
