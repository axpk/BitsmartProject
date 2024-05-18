from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler

print(f"Tensorflow version: {tf.__version__}")


model = tf.keras.models.load_model('model.keras')
app = Flask(__name__)


def preprocess_data(today_date):
    end_date = datetime.strptime(today_date, '%Y-%m-%d') + timedelta(days=1)  # YF data exclusive, so today + 1
    data = yf.download('BTC-USD', start="2014-09-17", end=end_date.strftime('%Y-%m-%d'))
    data = data[['High', 'Low', 'Close']].values
    scaler = MinMaxScaler()
    train_size = len(data) - 59
    scaler.fit(data[0:train_size, :])  # To keep consistent with scaler in training
    test_data = scaler.transform(data[-30:, :])
    input_data = np.array([test_data])
    return input_data, scaler


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        today_date = data['date']
        input_data, scaler = preprocess_data(today_date)
        future_pred = []

        for i in range(0,7):
            pred = model.predict(input_data)
            input_data = np.append(np.delete(input_data, 0, axis=1), [pred], axis=1)
            pred_unscaled = scaler.inverse_transform(pred)
            future_pred.append(pred_unscaled[0])

        future_pred = np.array(future_pred)
        highest_price_prediction = int(np.max(future_pred[:,0]))
        lowest_price_prediction = int(np.min(future_pred[:,1]))
        avg_closing_prediction = int(np.mean(future_pred[:,2]))

        response = { # TODO - Add Swing Trading Strategy
            'highest_price': highest_price_prediction,
            'lowest_price': lowest_price_prediction,
            'avg_closing_price': avg_closing_prediction
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
