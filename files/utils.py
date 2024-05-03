import json


def get_feature_collection(chunks):
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    for chunk in chunks:
        feature_collection["features"].append(
            get_feature(chunk.json["properties"]["id"], chunk.json["geometry"]))
    return feature_collection


def get_feature(id, geometry):
    return {
        "type": "Feature",
        "properties": {
            "id": id
        },
        "geometry": geometry
    }
