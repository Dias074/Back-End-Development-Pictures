from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return jsonify(picture), 200
    return jsonify(message='Picture not found'), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json(silent=True)
    if not isinstance(picture, dict) or type(picture.get('id')) is not int:
        return jsonify(message='A JSON picture with an integer id is required'), 400
    if any(item['id'] == picture['id'] for item in data):
        return jsonify(Message=f"picture with id {picture['id']} already present"), 302
    required = {'pic_url', 'event_country', 'event_state', 'event_city', 'event_date'}
    if not required.issubset(picture):
        return jsonify(message='Missing picture fields'), 400
    data.append(picture)
    response = jsonify(picture)
    response.status_code = 201
    response.headers['Location'] = url_for('get_picture_by_id', id=picture['id'])
    return response

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updates = request.get_json(silent=True)
    if not isinstance(updates, dict):
        return jsonify(message='A JSON object is required'), 400
    if 'id' in updates and updates['id'] != id:
        return jsonify(message='Picture id cannot be changed'), 400
    for picture in data:
        if picture['id'] == id:
            picture.update(updates)
            return jsonify(picture), 200
    return jsonify(message='Picture not found'), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture['id'] == id:
            del data[index]
            return '', 204
    return jsonify(message='Picture not found'), 404
