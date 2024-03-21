from flask import Flask, jsonify, request
import joblib
import keras
import utils as utils
import search as search
import parse as parse
import json
import copy
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

iso_forest_model = joblib.load('models/anomaly_detector_v3.joblib')

w2vModel = joblib.load('models/word2vec_lower.joblib')
classifier = model =keras.models.load_model('models/classifier_v2_bidirectional')

vocab_wv = w2vModel.wv.index_to_key

# w2vModel, vocab_wv, iso_forest_model, classifier,
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask API'})


@app.route('/api/parse', methods=['POST'])
def get_data():
        json_schema = {}
        if 'report' not in request.files:
            return 'Report invalid/missing', 400
        report = request.files['report']
        report_content = report.read()
        json_report = json.loads(report_content.decode('utf-8'))
        
        if 'schema' not in request.files:
            json_schema = search.search(copy.deepcopy(json_report),w2vModel, vocab_wv, iso_forest_model, classifier)
            print(json_report)
        else:
            schema = request.files['schema']
            schema_content = schema.read()
            json_schema = json.loads(schema_content.decode('utf-8'))
        
        output = parse.extract(json_schema, json_report, [])




        return jsonify({'report': output,'schema':json_schema})
if __name__ == '__main__':
    app.run(debug=True)