from flask import Flask, jsonify, request, render_template
import numpy as np
import json
import pickle
from data_input import data_in


def load_models():
    file_name = "models/model.pkl"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model


app = Flask(__name__)
@app.route('/predict', methods = ['GET'])
def predict():
    # stub input features
    x = np.array(data_in).reshape(1,-1)
    #x_in = np.array(x).reshape(1,-1)
    # load model
    model = load_models()
    prediction = model.predict(x)[0]
    response = json.dumps({'response': prediction})
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)