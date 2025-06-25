# ❤️ Heart Disease Risk Assessment Web App

!(static/images/screenshot.png)  
*A machine learning-powered web application to assess your risk of heart disease*

## 🚀 Overview
This project combines medical research with machine learning to create an accessible heart disease risk assessment tool. Based on the UCLA Heart Disease dataset and my research paper findings, this app provides personalized risk predictions with explanations.

## ✨ Features
- 🧠 **ML-Powered Predictions**: Logistic Regression model trained on clinical data
- 📱 **Responsive Design**: Works on desktop, tablet & mobile
- 📊 **Risk Visualization**: Clear risk levels with explanations
- 🔍 **Feature Importance**: Shows top contributing factors
- 💡 **Personalized Recommendations**: Tailored health advice

## 🛠️ Technologies Used
### Core Stack
- **Frontend**: 
  ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black)
  ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white)

- **Backend**: 
  ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
  ![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
  ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white)
  ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white)

### Design Elements
- 🎨 Custom CSS animations (beating heart, risk cards)
- ✨ Font Awesome icons
- 📱 Fully responsive mobile menu

## 📚 Research Foundation
### UCLA Heart Disease Dataset
- Contains **303 patient records** with **13 clinical features**
- Collected at UCLA Medical Center
- Key features include:
  - Age, sex, blood pressure
  - Cholesterol levels
  - ECG results
  - Exercise-induced angina
  - ST depression
  - Thalassemia

### Model Development
- **Algorithm**: Logistic Regression (85% accuracy)
- **Feature Engineering**:
  - Age groups categorization
  - Cholesterol level classification
  - One-hot encoding for categorical variables
- **Validation**: 5-fold cross validation

## 🏗️ Project Structure
heart-disease-app/
├── static/
│ ├── css/
│ │ ├── style.css
│ │ ├── assessment.css
│ │ └── result.css
│ ├── js/
│ │ └── heart-animation.js
│ └── images/
├── templates/
│ ├── index.html
│ ├── assessment.html
│ └── result.html
├── models/
│ ├── heart_disease_model.pkl
│ ├── heart_disease_scaler.pkl
│ └── feature_names.pkl
├── app.py
└── requirements.txt


## 🚦 Getting Started
### Prerequisites
- Python 3.8+
- pip or conda

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/amrita060404/heart-disease-risk-app.git
   cd heart-disease-risk-app

2. Create the virtual environment:
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
  pip install -r requirements.txt
    (anaconda asked me not to use pip as it will break the dependencies in spyder, used conda prompt)

4. Run the app:
   python app.py
   
6. Open in browser:
   http://localhost:5000
    (I used 5001 as 5000 was giving me some weird issues like bot requests??)
   
## 📝 Key Learnings
Through developing this project, I:
- 🔍 Gained deeper understanding of cardiovascular risk factors
- 🤖 Improved my feature engineering skills
- 🌐 Learned to deploy ML models in web apps
- 🎨 Developed better UI/UX design skills
- 📊 Understood the importance of model interpretability

## ⚠️ Important Disclaimer
-❗ This tool provides risk prediction only and is not a substitute for professional medical advice. Always consult with a healthcare provider for medical decisions.

Developed with ❤️ by Amrita Yadav
https://img.shields.io/badge/-GitHub-181717?logo=github
https://img.shields.io/badge/-LinkedIn-0077B5?logo=linkedin



