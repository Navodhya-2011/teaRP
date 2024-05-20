from flask import Flask, request, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pickle

app = Flask(__name__)


model_path = 'model_fit.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load your dataset
df = pd.read_excel('C:/Users/Navodhya Yasisuru/OneDrive/Documents/RP1/adjusted_tea_production_data.xlsx', engine='openpyxl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    future_date = pd.to_datetime(data['date'])
    tea_grade = data['tea_grade']

    try:
        # Preprocess the DataFrame based on the incoming tea_grade
        grade_df = df[df['Tea Grade'] == tea_grade].copy()
        grade_df.sort_values(by='Date', inplace=True)
        grade_df.set_index('Date', inplace=True)

        # Check if the future_date is indeed in the future and perform prediction
        if future_date > grade_df.index[-1]:
            model = ARIMA(grade_df['Quantity (kg)'], order=(5,1,0))
            model_fit = model.fit()

            future_steps = (future_date - grade_df.index[-1]).days
            forecast = model_fit.get_forecast(steps=future_steps)
            predicted_value = forecast.predicted_mean[-1]

            return jsonify({
                'grade': tea_grade,
                'future_date': future_date.strftime('%Y-%m-%d'),
                'predicted_quantity_kg': predicted_value
            })
        else:
            return jsonify({'error': 'The provided date is not in the future based on the dataset.'}), 400

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Error making prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)






# from flask import Flask, request, jsonify
# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# import pickle
# import json

# app = Flask(__name__)

# # Load your trained ARIMA model (adjust the path as needed)
# model_path = 'model_fit.pkl'
# with open(model_path, 'rb') as file:
#     model = pickle.load(file)


#     # Load the DataFrame here
    
#     # Your existing prediction logic

# @app.route('/predict', methods=['POST'])
# def predict():
#     df = pd.read_csv('C:/Users/Navodhya Yasisuru/OneDrive/Documents/RP1/adjusted_tea_production_data.xlsx')

#     data = request.get_json(force=True)
    
#     # Extract and process the input data
#     future_date = pd.to_datetime(data['date'])
#     tea_grade = data['tea_grade']
    
#     # Assuming df is your DataFrame containing the historical data
#     grade_df = df[df['Tea Grade'] == tea_grade].copy()
#     grade_df.sort_values(by='Date', inplace=True)
#     grade_df.set_index('Date', inplace=True)

#     # Fit and forecast (This part should ideally be pre-calculated, and the model loaded directly)
#     model = ARIMA(grade_df['Quantity (kg)'], order=(5,1,0))
#     model_fit = model.fit()
#     future_steps = (future_date - grade_df.index[-1]).days

#     forecast, forecast_index = None, None
#     if future_steps > 0:
#         forecast = model_fit.get_forecast(steps=future_steps).predicted_mean
#         forecast_index = pd.date_range(start=grade_df.index[-1], periods=future_steps + 1, freq='D')[1:].strftime('%Y-%m-%d').tolist()
    
#     return jsonify({
#         'grade': tea_grade,
#         'future_date': future_date.strftime('%Y-%m-%d'),
#         'forecast_dates': forecast_index,
#         'forecast_values': forecast.tolist() if forecast is not None else []
#     })

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Load the DataFrame here
#     df = pd.read_csv('C:/Users/Navodhya Yasisuru/OneDrive/Documents/RP1/adjusted_tea_production_data.xlsx')

#     # Your existing prediction logic