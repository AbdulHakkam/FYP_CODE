def extract(schema, data, output, isNewObj = False,path=''):
    if isinstance(schema, list):
        schema = {
            "data":schema,
        }
        data = {
            "data":data,
        }
    buffer = {}
    foundStart = False
    for key, value in schema.items():


        if key[-1]=='$':
            isNewObj = True
            foundStart = True
            key = key[:-1]
        
        newPath = path
        pathKey = key


        if isinstance(value,list):
            pathKey = pathKey + '[]'
        if path == '':
            newPath = pathKey
        else:
            newPath = newPath +"."+ pathKey
        
        if key not in data:
            continue

        if isinstance(value, dict):
           extracted = extract(value, data[key], output, isNewObj,newPath)
           if isNewObj:
               buffer.update(extracted)
        if isinstance(value, list):
            for item in data[key]:
                extracted = extract(value[0], item,  output,isNewObj,newPath)
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
        if isinstance(value, str):
            buffer[value] = data[key]

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