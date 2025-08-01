from flask import Flask,request,jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)
model = joblib.load('LR_Model/medical_insurance_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        age = data.get('age')
        smoker = data.get('smoker')
        bmi = data.get('bmi')

        ip = {
            'age'         :age,
            'smoker_no'   :1 if smoker=='no' else 0,
            'smo_bmi_low' :1 if smoker=='yes' and bmi<=30 else 0,
            'smo_bmi_high':1 if smoker=='yes' and bmi>30 else 0
        }

        df = pd.DataFrame([ip])
        prediction = model.predict(df)[0]
        return jsonify({'prediction':prediction})
    except Exception as e:
        return jsonify({'error':str(e)}),400

if __name__ == '__main__':
    app.run(debug = True)