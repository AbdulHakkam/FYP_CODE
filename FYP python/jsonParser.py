import json

def extract_data(json_obj, key):
    extracted_data = []

    if isinstance(json_obj, dict):
        if key in json_obj:
            extracted_data.append(json_obj)
        for k, v in json_obj.items():
            extracted_data.extend(extract_data(v, key))
    elif isinstance(json_obj, list):
        for item in json_obj:
            extracted_data.extend(extract_data(item, key))

    return extracted_data

def main(json_file, key):
    with open(json_file, 'r') as file:
        data = json.load(file)

    extracted_data = extract_data(data, key)

    if extracted_data:
        print("Extracted Data:")
        for item in extracted_data:
            print(item)
    else:
        print(f"No data found with key '{key}'.")

# Example usage:
json_file_path = 'redis_1.json'
desired_key = 'Target'

main(json_file_path, desired_key)