from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from flask_cors import CORS

print(f"Tensorflow version: {tf.__version__}")


model = tf.keras.models.load_model('model.keras')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def preprocess_data(today_date):
    end_date = datetime.strptime(today_date, '%Y-%m-%d') + timedelta(days=1)  # YF data exclusive, so today + 1
    data = yf.download('BTC-USD', start="2014-09-17", end=end_date.strftime('%Y-%m-%d'))
    data = data[['High', 'Low', 'Close']].values
    last_closed_price = data[-1][2]
    scaler = MinMaxScaler()
    train_size = len(data) - 59
    scaler.fit(data[0:train_size, :])  # To keep consistent with scaler in training
    test_data = scaler.transform(data[-30:, :])
    input_data = np.array([test_data])
    return input_data, scaler, last_closed_price

@app.route('/test', methods=['GET'])
def test():
    return "Hello World!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        today_date = data['date']
        input_data, scaler, last_closed_price = preprocess_data(today_date)
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

        print("Predicted prices for upcoming week from today:")
        for i in range(len(future_pred)):
            print(future_pred[i])

        print("Last Closed Price: ", last_closed_price)
        print("Calculating Swing Trading Strategy...")

        highest_avg_date_index = np.argmax(future_pred[:, 2])
        sell_date = None
        load_date = None
        sold_index = 0

        # Check to see if worth selling
        if future_pred[highest_avg_date_index, 2] > last_closed_price:
            sell_date = (datetime.strptime(today_date, '%Y-%m-%d') + timedelta(days=int(highest_avg_date_index))).strftime('%Y-%m-%d')
            sold_index = highest_avg_date_index
        else:
            # sell_date = "NA" # hold if today's price is highest
            sell_date = (datetime.strptime(today_date, '%Y-%m-%d')).strftime('%Y-%m-%d') # sell if today's price is highest

        # If sold, check to see if worth re-buying this week
        if sell_date and sell_date != 'NA':
            if sold_index >= 6:
                load_date = "NA"
            else:
                lowest_avg_date_index = np.argmin(future_pred[sold_index:, 2])
                load_date = (datetime.strptime(today_date, '%Y-%m-%d') + timedelta(days=int(lowest_avg_date_index))).strftime('%Y-%m-%d')

        # If sell_date was never set
        if not sell_date:
            sell_date = "NA"

        # If load_date was never set
        if not load_date:
            load_date = "NA"

        response = {
            'highest_price': highest_price_prediction,
            'lowest_price': lowest_price_prediction,
            'avg_closing_price': avg_closing_prediction,
            'sell_date': sell_date,
            'load_date': load_date
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(port=8000, debug=True)
