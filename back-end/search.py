import keras
import utils as utils
import re


map= {
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

def clearMap():
    global map
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

def parse( data,w2vModel, vocab_wv, iso_forest_model, classifier, path='', ):
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
           parse( data[key], w2vModel, vocab_wv, iso_forest_model, classifier,newPath)


        if isinstance(value, list):
            if(len(data[key])>2):
                data[key] = data[key][:3]
            for item in data[key]:
                if isinstance(item, dict):
                    parse( item,w2vModel, vocab_wv, iso_forest_model, classifier, newPath)
        
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


def search(data,w2vModel, vocab_wv, iso_forest_model, classifier):
    clearMap()
    global map
    parse(data,w2vModel, vocab_wv, iso_forest_model, classifier)
    sorted_keys = sorted(map, key=lambda k: len(map[k]['path'].split('...')))
    map = {k: map[k] for k in sorted_keys}
    map[sorted_keys[0]]['path'] = map[sorted_keys[0]]['path'] + '$'
    schema = generateSchema()
    print(schema)
    return schema