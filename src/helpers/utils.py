from boto3.dynamodb.types import TypeDeserializer

serializer = TypeDeserializer()

def deserialize(data):
    if isinstance(data, list):
       return [deserialize(v) for v in data]

    if isinstance(data, dict):
        try: 
            return serializer.deserialize(data)
        except TypeError:
            result = {}
            for key, val in data.items():
                result[key] = serializer.deserialize(val)
            return result

    else:
        return data