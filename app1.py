from flask import Flask, request, render_template
import pickle
import numpy as np  # Import numpy

app = Flask(__name__)

# Load your trained model
with open('trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')  # Optional: a home page if needed

@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        data = request.get_json()
    else:
        # Assume form submission
        data = request.form.to_dict()

    # Extract input values from JSON or form
    try:
        features = np.array([
            float(data['age']), float(data['sex']), float(data['cp']), float(data['trestbps']),
            float(data['chol']), float(data['fbs']), float(data['restecg']), float(data['thalch']),
            float(data['exang']), float(data['oldpeak']), float(data['slope']), float(data['ca']),
            float(data['thal'])
        ]).reshape(1, -1)  # Reshape for a single sample
    except KeyError as e:
        return render_template('error.html', message=f"Missing required field: {e}")  # Render an error page

    # Prediction
    prediction = model.predict(features)[0]  # Use numpy array
    probabilities = model.predict_proba(features)[0]  # Use numpy array

    # Render result.html with the prediction data
    return render_template(
        'result.html',
        prediction=int(prediction),
        probabilities=probabilities.tolist(),
        user_data=data
    )

if __name__ == '__main__':
    app.run(debug=True)

