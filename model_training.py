# -*- coding: utf-8 -*-
"""model_training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10y5UbNLc_D-toDXAUIR9En75lFunxfvj

## Initial Steps

Import the libraries.
"""

#import libraries

#1. to handle the data
import pandas as pd
import numpy as np
#2. to visualize the data
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
#3. to pre-process the data
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer,KNNImputer
#import iterative imputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
#4. to train the model in ML
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score
#5. for classification tasks
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.svm import SVC
#5a. metrics
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import sklearn
print(sklearn.__version__)


#ignore warnings
import warnings
warnings.filterwarnings('ignore')



# Load the dataset (replace delimiter if needed)
data_path = "heart_disease_uci.csv"

df = pd.read_csv(data_path)

# Display the first few rows
print(df.head())

"""## Exploratory Data Analysis

Preview the Data
"""

#explore each column's datatypes and missing values
df.info()

"""We have missing values in the following variables:

ca
thal
But we'll deal with these missing values in the next steps.
"""

#check the shape of dataset
df.shape

"""Explore Each Column

ID
"""

#find min and max value of id variable
df['id'].min(), df['id'].max()

#is there any id number duplicate?
df['id'].nunique()
#Answer: No, there are unique id number in each row.

"""age"""

#smmary statistics of 'age' variable

df['age'].describe()

#minimum and maximum age for heart disease
print("The minimum age for heart disease diagnosis is: ",df['age'].min())
print("The maximum age for heart disease diagnosis is: ",df['age'].max())

#plot distribution of age column
plt.figure()
sns.histplot(data=df, x='age', kde=True,color='green')
plt.title('Age Distribution')
plt.xlabel('Age')
plt.show()

#plot the mean,median and mode of age column to check at which age, most people suffer from heart disease
plt.figure()
sns.histplot(df['age'],kde=True,color='yellow')
plt.axvline(df['age'].mean(),color='red')
plt.axvline(df['age'].median(),color='green')
plt.axvline(df['age'].mode()[0],color='blue')
plt.show()

#print mean, median and mode
print("The mean of age is: ", df['age'].mean())
print("The median of age is: ", df['age'].median())
print("The mean of age is: ",df['age'].mode()[0])

#Answer is: 53-54 years old people are mostly suffer from heart disease.

#lets check the age based on gender | who suffer from heart disease mostly? (male or female)
fig = px.histogram(data_frame=df, x='age', color='sex')
fig.show()

#Answer: Mostly males are suffer from heart disease than females at the age of 54-55 years. But how? Lets see in the next step.

"""sex"""

#lets check the value count of sex variable in this data
df['sex'].value_counts()

#males are in greater amount than females

#calculate the percentage of male & female value counts in data
male_count = 206
female_count = 97
total_count = male_count + female_count
#total count=920
#male percentage
male_percentage = (male_count/total_count) * 100
print("The percentage of male's value count in data is:", round(male_percentage,2),'%')
#female percentage
female_percentage = (female_count/total_count) * 100
print("The percentage of female's value count in data is:", round(female_percentage,2),'%')

#plot percentages through barplot
plt.figure()
sns.barplot(x=['Male', 'Female'], y=[male_percentage, female_percentage])
plt.title('Percentage by Gender')
plt.xlabel('Gender')
plt.ylabel('Percentage')
plt.show()

"""dataset"""

#lets deal with 'dataset' variable
#find places where this data is collected
df['dataset'].value_counts()

"""We have highest number of records collected from Cleveland and the lowest number of records collected from Switzerland"""

#plot the countplot of dataset variable
plt.figure()
sns.countplot(data=df,x='dataset')
plt.show()

#lets find the sex ratio through groupby method in places where data is collected
df.groupby('dataset')['sex'].value_counts()

#plot this ratio
plt.figure()
sns.countplot(data=df, x='dataset', hue='sex')
plt.title('Gender Count by Dataset')
plt.xlabel('Dataset')
plt.ylabel('Count')
plt.legend(title='Sex', labels=['Female', 'Male'])
plt.show()

"""The highest number of females in this dataset are from Cleveland (97) and the lowest no. of females are from VA Long Beach (6)
The highest number of males in this dataset are from Hungary (212) and the lowest no. of males are from Switzerland (113)

cp(chest pain)
"""

#let's find how many types are in cp variable
df['cp'].nunique()
#answer---> 4

#let's find what are those 4 types
df['cp'].unique()

"""Typical Angina: Chest pain caused by reduced blood flow to the heart, usually triggered by physical exertion or stress.
Asymptomatic: No noticeable chest pain or symptoms, even if there's underlying heart disease.
Non-Anginal: Chest pain not related to heart problems, often caused by conditions like acid reflux or muscle strain.
Atypical Angina: Chest pain with unusual symptoms, such as discomfort not directly linked to exertion or classic angina triggers.
"""

#lets find value count of these types in data
df['cp'].value_counts()

# Group by 'cp' and 'age' and count values
grouped = df.groupby('cp')['age'].value_counts()

# Unstack the grouped result to ensure all 'cp' types are represented as columns
grouped_unstacked = grouped.unstack(level=0, fill_value=0)

# Display the result
print(grouped_unstacked)

plt.figure(figsize=(10, 6))
sns.heatmap(grouped_unstacked, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Age Distribution by CP')
plt.xlabel('CP Type')
plt.ylabel('Age')
plt.show()

#countplot of cp column group by sex variable
plt.figure()
sns.countplot(df, x='cp', hue='sex')
plt.show()

"""asymptomatic in males are larger compared to females. now the question is, in which dataset (place), asymptomatic data was maximum found."""

#countplot of cp column group by dataset variable
plt.figure()
sns.countplot(df, x='cp', hue='dataset')
plt.show()

"""This graph shows that mostly data of asymptomatic collected from "Cleveland"

trestbps
"""

#preview the trestbps
df['trestbps'].head()

#summary statistics of trestbps
df['trestbps'].describe()

#create a histplot of trestbps column
plt.figure()
sns.histplot(data=df, x='trestbps',kde=True)
plt.show()

#missing values check
df['trestbps'].isnull().sum()

# Group by 'sex' and count occurrences of 'trestbps'
grouped_trestbps = df.groupby('sex')['trestbps'].value_counts()

# Unstack the grouped result to ensure all 'sex' values are represented as columns
grouped_trestbps_unstacked = grouped_trestbps.unstack(level=0, fill_value=0)

# Display the result
print(grouped_trestbps_unstacked)

plt.figure(figsize=(10, 6))
sns.heatmap(grouped_trestbps_unstacked, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Trestbps Distribution by Sex')
plt.xlabel('Sex')
plt.ylabel('Trestbps')
plt.show()

"""chol"""

# Check if there are cholesterol values equal to 0
chol_zero_count = df['chol'].value_counts().loc[0] if 0 in df['chol'].values else 0
print(f"Number of records with cholesterol level 0: {chol_zero_count}")

# Display overall distribution for context
print("Cholesterol Value Distribution:")
print(df['chol'].value_counts().sort_index())

plt.figure(figsize=(10, 6))
sns.histplot(df['chol'], bins=30, kde=True, color='blue')
plt.axvline(x=0, color='red', linestyle='--', label='Cholesterol = 0')
plt.title('Distribution of Cholesterol Levels')
plt.xlabel('Cholesterol Level')
plt.ylabel('Frequency')
plt.legend()
plt.show()

"""fbs"""

df['fbs']

df['restecg'].value_counts()

df['restecg'].isnull().sum()

#restecg based on gender
df.groupby('sex')['restecg'].value_counts()

plt.figure()
sns.countplot(data=df, x='restecg', hue='sex')
plt.show()

print(df['thalch'].min()) #minimum
print(df['thalch'].max()) #maximum

df['exang']

"""oldpeak"""

print(df['oldpeak'].min())
print(df['oldpeak'].max())

"""slope"""

df['slope'].value_counts()

"""Flat: Indicates no significant change in the ST segment during exercise, often associated with a higher risk of heart disease.

Upsloping: The ST segment rises during exercise, which is generally considered a normal response or less indicative of severe heart issues.

Downsloping: The ST segment drops during exercise, strongly associated with ischemia (insufficient blood flow to the heart) and heart disease risk.

The counts indicate how many patients in the dataset have each slope type, with flat slopes being the most common.

ca
"""

df['ca'].min()

df['ca'].max()

df['ca'].value_counts().head(4)

"""thal"""

df['thal'].value_counts()

#thal based on gender
df.groupby('sex')['thal'].value_counts()

#plot
sns.countplot(data=df, x='thal', hue= 'sex')

"""num"""

df['num'].describe()

# Count of unique values in `target`
print(df['num'].value_counts())

# Plot the distribution of `num` values
plt.figure()
sns.countplot(data=df, x='num', palette='viridis')
plt.title('Distribution of Heart Disease Severity (target)')
plt.xlabel('Heart Disease Severity (target)')
plt.ylabel('Count')
plt.show()

# Percentage distribution of `num`
percentage_distribution = df['num'].value_counts(normalize=True) * 100
print(percentage_distribution)

# Average age for each heart disease severity level
avg_age_per_target = df.groupby('num')['age'].mean()
print(avg_age_per_target)

"""Missing Values"""

#deal with missing values in trestbps column
print(f'The missing values in trestbps variable are: ',df['trestbps'].isnull().sum())

#percentage of missing values
print(f"The percentage of missing values in trestbps variable are: {df['trestbps'].isnull().sum()/len(df)*100:.2f}%")

#impute missing values using iterative imputer
imputer = IterativeImputer(max_iter=10,random_state=42)
#fit the imputer on trestbps
imputer.fit(df[['trestbps']])
#transform
df['trestbps'] = imputer.transform(df[['trestbps']])

#verify if the missing values are imputed or not
df['trestbps'].isnull().sum()

#find only categorical columns
cat_cols = df.select_dtypes(include='object').columns.tolist()
cat_cols

#find only numeric columns
num_cols = df.select_dtypes(exclude='object').columns.tolist()
num_cols

#find only boolean columns
bool_cols = df.select_dtypes(include='bool').columns.tolist()
bool_cols

(df.isnull().sum()/len(df) * 100).sort_values(ascending=False)

df.info()

# [ca,oldpeak, thalch, chol]---> These are columns that has numeric dtype
#impute missing values by iterative imputer
imputer_1 = IterativeImputer(max_iter=10,random_state=42)
#fit_transform the imputer
df[['ca','oldpeak','thalch','chol']] = imputer_1.fit_transform(df[['ca','oldpeak','thalch','chol']])

#check if the missing values are imputed or not
(df.isnull().sum()/len(df) * 100).sort_values(ascending=False)

"""thal"""

df['thal'].value_counts()

#plot 'thal' by sex variable
plt.figure()
sns.countplot(data=df, x='thal', hue='sex', palette={'Male': 'blue', 'Female': 'pink'})
plt.show()

#missing value %age in 'thal' varibale
print(f"The percentage of missing values in this variable is: {df['thal'].isnull().sum()/len(df) *100:.2f}%")

#lets impute missing values in thal column by ML models
#define the function
def impute_missing_values_with_rf(df, column_name):
    """
    Impute missing values in a categorical column using RandomForestClassifier.

    Parameters:
        df (pd.DataFrame): The input DataFrame with missing values.
        column_name (str): The name of the categorical column to impute.

    Returns:
        pd.DataFrame: The DataFrame with missing values imputed.
    """

    # Step 1: Create a copy of the original DataFrame to avoid modifying it directly
    df = df.copy()

    # Step 2: Check if the column has missing values
    if df[column_name].isnull().sum() == 0:
        print(f"No missing values in column '{column_name}' to impute.")
        return df

    print(f"Imputing missing values in column '{column_name}' with RandomForestClassifier...")

    # Step 3: Label encode the target column
    le = LabelEncoder()
    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].apply(lambda x: np.nan if x.lower() == 'nan' else x)

    # Encode non-null values
    non_null_data = df[df[column_name].notnull()]
    null_data = df[df[column_name].isnull()]

    if null_data.empty:
        print(f"No missing values in '{column_name}' after preprocessing.")
        return df

    # Encode the target variable
    non_null_data[column_name] = le.fit_transform(non_null_data[column_name].astype(str))

    # Step 4: Define features (X) and target (y)
    X = non_null_data.drop(columns=[column_name])
    y = non_null_data[column_name]

    # One-hot encode the features
    X_encoded = pd.get_dummies(X, drop_first=True)

    # Align features for the null_data set
    null_data_encoded = pd.get_dummies(null_data.drop(columns=[column_name]), drop_first=True)
    null_data_encoded = null_data_encoded.reindex(columns=X_encoded.columns, fill_value=0)

    # Check for any data availability
    if null_data_encoded.empty:
        print("No matching features found between training data and null data for prediction.")
        return df

    # Step 5: Train RandomForestClassifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=0)
    rf_model.fit(X_encoded, y)

    # Step 6: Predict missing values
    predicted_values = rf_model.predict(null_data_encoded)

    # Step 7: Decode the predicted values back to the original labels
    decoded_values = le.inverse_transform(predicted_values)

    # Step 8: Impute missing values in the original DataFrame
    df.loc[df[column_name].isnull(), column_name] = decoded_values

    print(f"Missing values in '{column_name}' have been imputed successfully.")
    return df

#impute missing values
df = impute_missing_values_with_rf(df, 'thal')

"""slope"""

#impute missing values by reusing the function
df = impute_missing_values_with_rf(df, 'slope')

"""exang"""

#impute missing values by reusing the function
df = impute_missing_values_with_rf(df, 'exang')

"""restecg"""

#impute missing values by reusing the function
df = impute_missing_values_with_rf(df, 'restecg')

"""fbs"""

#impute missing values by reusing the function
df = impute_missing_values_with_rf(df, 'fbs')

#verify if the dataset has missing values imputed or not
df.info()

"""Outliers"""

#boxplot of numeric columns
plt.figure()
sns.boxplot(df['age'],color='red')
plt.show()

plt.figure()
sns.boxplot(df['thalch'],color='yellow')
plt.show()

plt.figure()
sns.boxplot(df['trestbps'],color='purple')
plt.show()

plt.figure()
sns.boxplot(df['oldpeak'],color='green')
plt.show()

plt.figure()
sns.boxplot(df['chol'],color='brown')
plt.show()

plt.figure()
sns.boxplot(df['ca'],color='blue')
plt.show()

plt.figure()
sns.boxplot(df['num'],color='red')
plt.show()

df[df['trestbps']==0]

#remove this row
df = df[df['trestbps'] != 0]

#check the dataset info
df.info()

#trestbps maximum outlier/extreme values
df[df['trestbps']>175]

#thalch variable outliers
print(df[df['thalch']<70])
print('---------------------')
print(df[df['thalch']>235])

df[df['oldpeak']<-2.55]

df[df['oldpeak']>4.25]

outliers = df[df['trestbps'] == 0]
print(outliers)  # Prints rows where 'trestbps' is 0

outliers = df[df['trestbps'] > 170]
print(outliers)

# Replace outliers with the median value of 'trestbps'
median_value = df['trestbps'].median()
df['trestbps'] = df['trestbps'].apply(lambda x: median_value if x > 170 else x)

outliers = df[df['oldpeak'] < 0]
print(outliers)

outliers = df[df['oldpeak'] > 4]
print(outliers)

# Replace outliers with the median of 'oldpeak'
median_value = df['oldpeak'].median()
df['oldpeak'] = df['oldpeak'].apply(lambda x: median_value if (x > 4 or x < 0) else x)

outliers = df[df['thalch'] < 70]
print(outliers)

median_value = df['thalch'].median()
df['thalch'] = df['thalch'].apply(lambda x: median_value if x < 94 else x)

outliers = df[df['chol'] > 370]
print(outliers)

median_value = df['chol'].median()
df['chol'] = df['chol'].apply(lambda x: median_value if (x > 370 or x < 100) else x)

outliers = df[df['ca'] > 1.75]
print(outliers)

median_value = df['ca'].median()
df['ca'] = df['ca'].apply(lambda x: median_value if x > 1.75 else x)



label_encoder = LabelEncoder()
df['cp'] = label_encoder.fit_transform(df['cp'])

sns.boxplot(df['cp'],color='pink')


"""Machine Learning"""

df.columns

# List of columns to encode
columns_to_encode = ['cp', 'sex', 'dataset', 'fbs', 'restecg', 'exang', 'slope', 'thal']

# Initialize label encoder and apply encoding
le_dict = {}  # Dictionary to store the label encoders
for col in columns_to_encode:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])  # Encode the column
    le_dict[col] = le  # Save the label encoder for potential inverse transformation later

plt.figure()
sns.countplot(data=df, x='cp', hue='sex')
plt.title('Chest Pain Type by Gender')
plt.show()


# Split the data into X and y
X = df.drop(columns=['id', 'dataset', 'num'], axis=1)
y = df['num']
print(X.columns)
#split the data into train, test and split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.35,random_state=42)

median_value = df['cp'].median()
df['cp'] = df['cp'].apply(lambda x: median_value if x < 2 else x)

outliers = df[df['cp'] < 2]
print(outliers)

df.info()

# Define models to train
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'Logistic Regression': LogisticRegression(random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(random_state=42),

}

# Train models and evaluate
results = []
for model_name, model in models.items():
    print(f"Training {model_name}...")
    try:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        results.append((model_name, acc))
        print(f"{model_name} Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))
    except Exception as e:
        print(f"Error training {model_name}: {e}")

# Select the best model
if results:
    best_model_name, best_model_score = max(results, key=lambda x: x[1])
    print("\nBest Model:")
    print(f"{best_model_name} with accuracy: {best_model_score:.4f}")
else:
    print("No valid model could be trained.")

"""Hyper Parameter Tuning"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

param_grid_rf = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
grid_rf = GridSearchCV(rf, param_grid_rf, cv=5, n_jobs=-1, scoring='accuracy')
grid_rf.fit(X_train, y_train)
best_rf = grid_rf.best_estimator_

# Predict using the best model found after hyperparameter tuning
y_pred = best_rf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")

# For a detailed classification report
print(classification_report(y_test, y_pred))

# Confusion Matrix (for classification problems)
print(confusion_matrix(y_test, y_pred))

#decision tree hyperparameter tuning
from sklearn.tree import DecisionTreeClassifier
param_grid_dt = {
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
dt = DecisionTreeClassifier(random_state=42)
grid_dt = GridSearchCV(dt, param_grid_dt, cv=5, n_jobs=-1, scoring='accuracy')
grid_dt.fit(X_train, y_train)
best_dt = grid_dt.best_estimator_

# Predict using the best model found after hyperparameter tuning
y_pred = best_dt.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")

# For a detailed classification report
print(classification_report(y_test, y_pred))

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot confusion matrix with better formatting
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1, 2, 3, 4], yticklabels=[0, 1, 2, 3, 4], cbar=False)

# Add labels, title, and axis ticks
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

"""To save the model."""

import pickle

# Save the best Decision Tree model to a file
with open('trained_model.pkl', 'wb') as f:
    pickle.dump(best_dt, f)

# Test loading the model
with open('trained_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Print the loaded model to verify
print("Model loaded successfully:", loaded_model)

# Test model predictions
sample_data = X_test.iloc[:1, :]  # Take a single test sample
prediction = loaded_model.predict(sample_data)
print("Sample Prediction:", prediction)

true_label = y_test.iloc[:1].values[0]
print("True Label:", true_label)

