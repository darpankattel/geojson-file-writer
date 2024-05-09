import json


def get_feature_collection(chunks):
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    for chunk in chunks:
        feature_collection["features"].append(
            get_feature(chunk.json["properties"]["id"], chunk.json["geometry"], chunk.json["properties"].get("green_field")))
    return feature_collection


def get_feature(id, geometry, green_field=None):
    return {
        "type": "Feature",
        "properties": {
            "id": id,
            "green_field": green_field
        },
        "geometry": geometry
    }
