import joblib
import argparse
import keras
import utils as utils
import json
import re

map = {
    "CVE":{
        "path":'',
        "score":0
    },
    "DESCRIPTION":{
        "path":'',
        "score":0
    },
    "SEVERITY":{
        "path":'',
        "score":0
    }
}

iso_forest_model = joblib.load('models/anomaly_detector_v3.joblib')

w2vModel = joblib.load('models/word2vec_lower.joblib')
classifier = model =keras.models.load_model('models/classifier_v2_bidirectional')

vocab_wv = w2vModel.wv.index_to_key


def parse( data, path=''):
    # Handle the case where data is a list and not an object
    if isinstance(data, list):
        data = {
            "data":data,
        }
    
    for key, value in data.items():  

        # Generate current path string
        newPath = path
        pathKey = key
        if isinstance(value,list):
            pathKey = pathKey + '[]'
        if path == '':
            newPath = pathKey
        else:
            newPath = newPath +"..."+ pathKey

        # Recursively iterate through the data
        if isinstance(value, dict):
           parse( data[key], newPath)


        if isinstance(value, list):
            if(len(data[key])>2):
                data[key] = data[key][:3]
            for item in data[key]:
                if isinstance(item, dict):
                    parse( item, newPath)
        
        # If end of object root is reached then predict
        if isinstance(value, str):
            val = re.sub(r'\d+', 'number', value)
            val = ' '.join(newPath.lower().split("...")) +" " + str(val)
            tokenized_test = [text.split() for text in [val]]
            vectorized_test = [utils.average_word_vectors(text, w2vModel, vocab_wv, 100) for text in tokenized_test]
            is_outlier = iso_forest_model.predict(vectorized_test)[0] == -1
            if not is_outlier:
                print(val)
                prediction = classifier.predict([val])[0]
                print(prediction)
                highest = max(prediction)
                index_of_highest = prediction.tolist().index(highest)
                if index_of_highest == 0 and highest > map["CVE"]["score"]:
                    map["CVE"]["path"] = newPath
                    map["CVE"]["score"] = highest
                elif index_of_highest == 1 and highest > map["DESCRIPTION"]["score"]:
                    map["DESCRIPTION"]["path"] = newPath
                    map["DESCRIPTION"]["score"] = highest
                elif index_of_highest == 2 and highest > map["SEVERITY"]["score"]:
                    map["SEVERITY"]["path"] = newPath
                    map["SEVERITY"]["score"] = highest

    return; 

def generateSchema():
    result = {}
    for key, value in map.items():
        parts = value['path'].split('...')
        current = result
        for i, part in enumerate(parts[:-1]):
            if part.endswith('[]'): 
                part = part[:-2]  
                if part not in current:
                    current[part] = [] 
                if not current[part]: 
                    current[part].append({})
                current = current[part][0]  
            else:
                if part not in current:
                    current[part] = {} 
                current = current[part] 

        last_part = parts[-1]
        if last_part.endswith('[]'):
            last_part = last_part[:-2] 
            if last_part not in current:
                current[last_part] = [] 
            current[last_part].append({})  
        else:
            current[last_part] = key 
    return result

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', type=str, required=True, help='Input file path')
parser.add_argument('--output', '-o', type=str,required=True, help='Output file path')
args = parser.parse_args()

with open(args.input, 'r',encoding="utf8") as data_file:
        # Load JSON data from file
        data = json.load(data_file)
        parse(data)
sorted_keys = sorted(map, key=lambda k: len(map[k]['path'].split('...')))
map = {k: map[k] for k in sorted_keys}
map[sorted_keys[0]]['path'] = map[sorted_keys[0]]['path'] + '$'
schema = generateSchema()

with open(args.output, 'w') as json_file:
    json.dump(schema,json_file, indent=2)