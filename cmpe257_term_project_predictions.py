# -*- coding: utf-8 -*-
"""CMPE257_Term_Project_Predictions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qPbUveK098juOgLdh5028JmuvsWrXHre
"""

import numpy as np
import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.layers import GlobalAveragePooling1D
import yfinance as yf

train_data = yf.download('BTC-USD', start="2014-09-17", end="2024-05-19")

data = yf.download('BTC-USD', start="2014-09-17", end="2024-" + input())

scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(train_data[['High', 'Low', 'Close']].values)

# train_size = len(data) - 59
# scaler = MinMaxScaler()
# scaler.fit(data[0:train_size,:])

data = data[['High', 'Low', 'Close']].values

test_data = scaler.transform(data[-30:,:])

model = tf.keras.models.load_model('model.keras')

input_data = np.array([test_data])

future_pred = []

for i in range(0,7):
    pred = model.predict(input_data)
    input_data = np.append(np.delete(input_data, 0, axis=1), [pred], axis=1)
    pred_unscaled = scaler.inverse_transform(pred)
    future_pred.append(pred_unscaled[0])
future_pred = np.array(future_pred)

with open("predictions.txt", "w") as f:
    for r in future_pred:
        for c in r:
            f.write(str(c) + ' ')
        f.write('\n')
    f.write(str(int(np.max(future_pred[:,0]))) + ' ')
    f.write(str(int(np.min(future_pred[:,1]))) + ' ')
    f.write(str(int(np.mean(future_pred[:,2]))) + ' ')

