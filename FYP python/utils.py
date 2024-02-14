import csv
import json
import xmltodict

def csv_to_json (csv_file_path, json_file_path):
    with open(csv_file_path, encoding='utf-8') as csvf: 
        csv_reader = csv.DictReader(csvf) 
        data = list(csv_reader) 
    with open(json_file_path, 'w', encoding='utf-8') as jsonf: 
        jsonf.write(json.dumps(data, indent=4))

def get_json_key_paths(json_obj, path=''):
    """
    Recursively find all paths to keys in a JSON object.

    :param json_obj: The JSON object (dict or list)
    :param path: The current path being processed
    :return: A list of paths to keys
    """
    key_paths = []

    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            new_path = f"{path}.{k}" if path else k
            key_paths.append(new_path)
            key_paths.extend(get_json_key_paths(v, new_path))
    elif isinstance(json_obj, list):
        for idx, item in enumerate(json_obj):
            new_path = f"{path}[]"
            key_paths.extend(get_json_key_paths(item, new_path))

    return key_paths

def xml_to_json(xml_file_path, json_file_path):
    with open(xml_file_path) as fd:
        doc = xmltodict.parse(fd.read())
    with open(json_file_path, 'w', encoding='utf-8') as jsonf: 
        jsonf.write(json.dumps(doc, indent=4))