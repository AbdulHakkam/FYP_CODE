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

non_outliers = []

keys_checked = 0



iso_forest_model = joblib.load('models/anomaly_detector_v3.joblib')

w2vModel = joblib.load('models/word2vec_lower.joblib')
classifier = model =keras.models.load_model('models/classifier_v2_bidirectional')

vocab_wv = w2vModel.wv.index_to_key


def parse( data, path=''):
    global keys_checked
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
            keys_checked += 1
            if not is_outlier:
                prediction = classifier.predict([val], verbose = 0)[0]
                non_outliers.append(newPath)
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


def sortMap():
    sorted_keys = sorted(map, key=lambda k: len(map[k]['path'].split('...')))
    map = {k: map[k] for k in sorted_keys}
    map[sorted_keys[0]]['path'] = map[sorted_keys[0]]['path'] + '$'

def clear():
    global map
    global non_outliers
    global keys_checked
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
    non_outliers = []
    keys_checked = 0

def evaluate():
    eval_files = [
        {
            "path":'reports/blackduck.json',
            "valid_paths":["data[]...Vulnerability id","data[]...Description","data[]...Severity","data[]...Security Risk"]
        },
        {
            "path":'reports/jfrog.json',
            "valid_paths":['data[]...component_versions...more_details...cves[]...cve','data[]...component_versions...more_details...description','data[]...severity']
        },
        {
            "path":'reports/jfrogArtifact.json',
            "valid_paths":["artifacts[]...issues[]...description","artifacts[]...issues[]...severity","artifacts[]...issues[]...cves[]...cve","artifacts[]...issues[]...summary"]
        },
        {
            "path":'reports/mongo_1.json',
            "valid_paths":["Results[]...Vulnerabilities[]...VulnerabilityID","Results[]...Vulnerabilities[]...Description", "Results[]...Vulnerabilities[]...Severity"]
        },
                {
            "path":'reports/postgres_1.json',
            "valid_paths":["Results[]...Vulnerabilities[]...VulnerabilityID","Results[]...Vulnerabilities[]...Description", "Results[]...Vulnerabilities[]...Severity"]
        }

    ]

    for file in eval_files:
        with open(file['path']) as f:
            data = json.load(f)
            parse(data)
            invalid_paths=0
            initial = len(non_outliers)

            for path in file['valid_paths']:
                if path in non_outliers:
                    non_outliers.remove(path)

            for data in map:
                if map[data]['path'] not in file['valid_paths']:
                    invalid_paths+=1    
        
            print("Outlier detection accuracy for  = ",[file['path']], (len(non_outliers)/initial)*100, "%")
            if invalid_paths > 0:
                print("Invalid paths in schema = ", invalid_paths)
            else :
                print("Schema is valid")
            clear()

evaluate()