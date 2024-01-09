import json

def extract(schema, data, output, isNewObj = False):
    buffer = {}
    foundStart = False
    for key, value in schema.items():
        if key[-1]=='$':
            isNewObj = True
            foundStart = True
            key = key[:-1]
            
        if key not in data:
            continue

        if isinstance(value, dict):
           extracted = extract(value, data[key], output, isNewObj)
           if isNewObj:
               buffer.update(extracted)
        if isinstance(value, list):
            for item in data[key]:
                extracted = extract(value[0], item,  output,isNewObj)
                if isNewObj :
                    if isinstance(extracted, dict):
                        for key in extracted.keys():
                            if key not in buffer:
                                buffer[key] = []
                            buffer[key].append(extracted[key])
                    else:
                        buffer.update(extracted)
            for key in buffer.keys():
                if isinstance(buffer[key], list) and len(buffer[key])==1:
                    buffer[key] = buffer[key][0]
            # if isNewObj:
            #         buffer.update(extracted)
        if isinstance(value, str):
            buffer[value] = data[key]
    # print("Buffer-------",buffer)
    # print("output-------",output)

    if foundStart and len(buffer)>0:
        output.append(buffer)
        return output
    elif isNewObj:
        return buffer
    else:
        if(len(buffer)>0):
            for item in output:
                item.update(buffer)
        return output
            
# Open the JSON file
with open('nvdReport.json', 'r',encoding="utf8") as schema_file:
    # Load JSON data from file
    schema = json.load(schema_file)

with open('response.json', 'r',encoding="utf8") as data_file:
        # Load JSON data from file
        data = json.load(data_file)
        x = extract(schema,data,[])
        print(len(x))
        with open('data.json', 'w') as json_file:
            json.dump(x,json_file, indent=2)