import json

def extract(schema, data,output):
    buffer = {}
    new_output = []
    for key,value in schema.items():
        if key in data:
            if isinstance(value, dict):
                new_output = extract(value, data[key],output)
                print(new_output)
            elif isinstance(value, list):
                for item in data[key]:
                    new_output = extract(value[0],item,new_output)
                    print(new_output)
            elif isinstance(value, str):
                buffer[value] = data[key]
    
    if len(new_output) > 0:
        for item in new_output:
            item.update(buffer)
        return new_output
    elif len(new_output) > 0:
        return new_output
    else:
        return output
            
# Open the JSON file
with open('trivySchema.json', 'r',encoding="utf8") as schema_file:
    # Load JSON data from file
    schema = json.load(schema_file)

with open('response.json', 'r',encoding="utf8") as data_file:
        # Load JSON data from file
        data = json.load(data_file)
        x = extract(schema,data,[])
        print(len(x))
        with open('data.json', 'w') as json_file:
            json.dump(x,json_file, indent=2)