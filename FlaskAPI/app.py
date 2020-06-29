from flask import Flask, jsonify, request, render_template
import numpy as np
import json
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    
    output = prediction
    
    return render_template('index.html', prediction_text = 'House rent would be ${}'.format(output))

if __name__ == '__main__':
 app.run(debug=True)
