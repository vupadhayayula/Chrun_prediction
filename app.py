from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model, scaler, and encoders
model = joblib.load(r'C:\Users\91630\Downloads\Flask\churn_model.pkl')
scaler = joblib.load(r'C:\Users\91630\Downloads\Flask\scaler.pkl')
label_encoders = joblib.load(r'C:\Users\91630\Downloads\Flask\label_encoders.pkl')

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form data
        form_data = {
            'Age': int(request.form['age']),
            'Gender': request.form['gender'],
            'ContractType': request.form['contract_type'],
            'MonthlyCharges': float(request.form['monthly_charges']),
            'TotalCharges': float(request.form['total_charges']),
            'TechSupport': request.form['tech_support'],
            'InternetService': request.form['internet_service'],
            'Tenure': int(request.form['tenure']),
            'PaperlessBilling': request.form['paperless_billing'],
            'PaymentMethod': request.form['payment_method'],
            'AverageMonthlyCharges': float(request.form['total_charges']) / int(request.form['tenure']),
            'CustomerLifetimeValue': float(request.form['monthly_charges']) * int(request.form['tenure']),
        }

        # Convert categorical data using LabelEncoders
        for col in ['Gender', 'ContractType', 'TechSupport', 'InternetService', 'PaperlessBilling', 'PaymentMethod']:
            form_data[col] = label_encoders[col].transform([form_data[col]])[0]

        # Convert to DataFrame
        input_data = pd.DataFrame([form_data])

        # Scale the numerical features
        input_data_scaled = scaler.transform(input_data)

        # Predict churn
        churn_prediction = model.predict(input_data_scaled)[0]
        churn_probability = model.predict_proba(input_data_scaled)[:, 1][0]

        # Display result
        prediction_text = "Yes" if churn_prediction == 1 else "No"
        return render_template('index.html', prediction=prediction_text, probability=round(churn_probability, 2))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
