from bson import ObjectId

def serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, list):
        return [serialize(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    else:
        return obj