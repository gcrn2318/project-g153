from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import warnings
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Suppress TensorFlow and warning logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.simplefilter("ignore", UserWarning)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True, allow_headers=['Content-Type'], methods=['GET', 'POST', 'OPTIONS'])

# Load and preprocess the data
data = pd.read_csv("data1.csv")
input_features = ['batting_team', 'bowling_team', 'venue']
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_categorical = encoder.fit_transform(data[input_features])

xfeats = ['over', 'ball']
scalerx = StandardScaler()
scaled_x = scalerx.fit_transform(data[xfeats])

yfeats = ['runs', 'wickets']
scalery = StandardScaler()
scaled_y = scalery.fit_transform(data[yfeats])

# Load the trained LSTM model
model = keras.models.load_model("lstm1.keras")

# Mapping for teams and venues
team = {1: 'Chennai Super Kings', 2: 'Delhi Capitals', 3: 'Gujarat Titans', 5: 'Kolkata Knight Riders', 6: 'Lucknow Super Giants', 7: 'Mumbai Indians', 9: 'Punjab Kings', 10: 'Rajasthan Royals', 12: 'Royal Challengers Bengaluru', 13: 'Sunrisers Hyderabad'}
venue = {1: 'Arun Jaitley Stadium', 3: 'Barsapara Cricket Stadium', 7: 'Dr DY Patil Sports Academy', 10: 'Eden Gardens', 11: 'Ekana Cricket Stadium', 12: 'Feroz Shah Kotla', 18: 'M Chinnaswamy Stadium', 19: 'MA Chidambaram Stadium', 20: 'Maharaja Yadavindra Singh International Cricket Stadium', 22: 'Narendra Modi Stadium', 27: 'Punjab Cricket Association IS Bindra Stadium', 28: 'Punjab Cricket Association Stadium', 29: 'Rajiv Gandhi International Stadium', 30: 'Sardar Patel Stadium', 31: 'Saurashtra Cricket Association Stadium', 32: 'Sawai Mansingh Stadium', 35: 'Sheikh Zayed Stadium', 37: 'Subrata Roy Sahara Stadium', 39: 'Vidarbha Cricket Association Stadium', 40: 'Wankhede Stadium'}
steam = {str(key): value for key, value in team.items()}
svenue = {str(key): value for key, value in venue.items()}

@app.route('/api/predict', methods=['POST'])
def predict_match():
    data = request.json
    print("Received request data:", data)  # Debugging log
    if not data:
        return jsonify({'error': 'No data provided.'}), 400

    try:
        teamA = int(data.get('teamA'))
        teamB = int(data.get('teamB'))
        venue1 = int(data.get('venue'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input format.'}), 400

    # Check if the same team is entered for both Team A and Team B
    if teamA == teamB:
        return jsonify({'error': 'Please provide two different teams as input.'}), 400

    if str(teamA) not in steam or str(teamB) not in steam or str(venue1) not in svenue:
        return jsonify({'error': 'Invalid team or venue code.'}), 400

    try:
        Input1 = [[teamA, teamB, venue1]]
        Input2 = [[teamB, teamA, venue1]]

        input_columns = ['batting_team', 'bowling_team', 'venue']
        Input1_df = pd.DataFrame(Input1, columns=input_columns)
        Input2_df = pd.DataFrame(Input2, columns=input_columns)

        scaled_input1 = encoder.transform(Input1_df)
        scaled_input2 = encoder.transform(Input2_df)

        Extrainput = [[19, 6]]
        scaled_extrainput = scalerx.transform(Extrainput)

        X_give1 = np.hstack((scaled_input1, scaled_extrainput))
        X_give1 = X_give1.reshape(X_give1.shape[0], 1, X_give1.shape[1])

        X_give2 = np.hstack((scaled_input2, scaled_extrainput))
        X_give2 = X_give2.reshape(X_give2.shape[0], 1, X_give2.shape[1])
    except Exception as e:
        return jsonify({'error': f'Error during input preparation: {str(e)}'}), 400

    try:
        pred1 = model.predict(X_give1, verbose=0)
        pred1 = scalery.inverse_transform(pred1).astype(float)  # Convert to float

        pred2 = model.predict(X_give2, verbose=0)
        pred2 = scalery.inverse_transform(pred2).astype(float)  # Convert to float
    except Exception as e:
        return jsonify({'error': f'Model prediction failed: {str(e)}'}), 500

    result = {
        'teamA': {
            'score': round(float(pred1[0, 0])),  # Explicit float conversion
            'wickets': round(float(pred1[0, 1])),  # Explicit float conversion
            'run_rate': round(float(pred1[0, 0]) / 20, 2)  # Explicit float conversion
        },
        'teamB': {
            'score': round(float(pred2[0, 0])),  # Explicit float conversion
            'wickets': round(float(pred2[0, 1])),  # Explicit float conversion
            'run_rate': round(float(pred2[0, 0]) / 20, 2)  # Explicit float conversion
        }
    }

    if pred1[0, 0] > pred2[0, 0]:
        result['teamB']['match_result'] = f"{steam[str(teamA)]} won by {round(float(pred1[0, 0] - float(pred2[0, 0])))} runs"
    else:
        result['teamB']['match_result'] = f"{steam[str(teamB)]} chased down the score"

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
