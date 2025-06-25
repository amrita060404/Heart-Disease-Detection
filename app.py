from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model, scaler, and feature names
model = joblib.load('models/heart_disease_model_20250624_183436.pkl')
scaler = joblib.load('models/heart_disease_scaler_20250624_183436.pkl')
feature_names = joblib.load('models/feature_names.pkl')

# Numerical features that need scaling
num_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        try:
            # Prepare input features in correct order
            input_features = []
            for feature in feature_names:
                value = request.form.get(feature)
                
                # Handle missing values (use median from training)
                if value in ['', None]:
                    if feature in num_features:
                        # Replace with median (you should pre-calculate these from your training data)
                        median_values = {
                            'age': 54,
                            'trestbps': 130,
                            'chol': 240,
                            'thalach': 150,
                            'oldpeak': 0.8
                        }
                        input_features.append(median_values.get(feature, 0))
                    else:
                        input_features.append(0)  # Default for categorical
                else:
                    input_features.append(float(value) if feature in num_features else float(value))
            
            # Convert to numpy array and reshape
            features_array = np.array(input_features).reshape(1, -1)
            
            # Scale numerical features
            features_df = pd.DataFrame(features_array, columns=feature_names)
            features_df[num_features] = scaler.transform(features_df[num_features])
            
            # Make prediction
            proba = model.predict_proba(features_df)[0][1]
            prediction = int(model.predict(features_df)[0])
            
            # Interpret probability
            risk_level = "low"
            if proba >= 0.7:
                risk_level = "high"
            elif proba >= 0.4:
                risk_level = "medium"
            
            # Get top 3 contributing features
            if hasattr(model.named_steps['model'], 'feature_importances_'):
                importances = model.named_steps['model'].feature_importances_
                top_features = sorted(zip(feature_names, importances), 
                                  key=lambda x: x[1], reverse=True)[:3]
            else:
                top_features = []
            
            return render_template('result.html', 
                                prediction=prediction,
                                probability=round(proba*100, 2),
                                risk_level=risk_level,
                                top_features=top_features)
        
        except Exception as e:
            return render_template('result.html', 
                                error=f"An error occurred: {str(e)}")
    
    # For GET request, show the form
    return render_template('assessment.html')

if __name__ == '__main__':
    app.run(debug=False, port=5001)