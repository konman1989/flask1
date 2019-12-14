from flask import Blueprint, Response, jsonify, request
from db_methods import get_db, update_db


people = Blueprint('people', __name__)


@people.route('/')
def get_people():
    country = request.args.get('country')
    db_content = get_db()

    if country is not None:
        list_ = [p for p in db_content['people'] if
                 p['country'].lower() == country.lower()]

        return jsonify(list_) if list_ else Response('Not Found', status=404)
    return jsonify(db_content['people'])


@people.route('/', methods=['POST'])
def post_people():
    person = request.get_json()
    db_content = get_db()

    max_id = max([p['id'] for p in db_content['people']])
    person_id = max_id + 1

    db_content['people'].append({'id': person_id, **person})
    update_db(db_content)
    return jsonify({'id': person_id}), 201


@people.route('/<int:id>')
def get_person(id):
    db_content = get_db()

    list_ = [p for p in db_content['people'] if p['id'] == id]
    return jsonify(list_) if list_ else Response('Not Found', status=404)


@people.route('/<int:id>', methods=['DELETE'])
def delete_person(id):
    db_content = get_db()
    try:
        item_to_delete = [p for p in db_content['people'] if p['id'] == id]
        db_content['people'].remove(item_to_delete[0])
        update_db(db_content)

        return Response(status=204)
    except IndexError:
        return Response('Not Found', status=404)


@people.route('/<int:id>', methods=['PATCH'])
def update_person(id):
    db_content = get_db()
    try:
        item_to_update = [p for p in db_content['people'] if p['id'] == id]
        index_to_update = db_content['people'].index(item_to_update[0])
        db_content['people'][index_to_update].update(request.get_json())
        update_db(db_content)

        return Response(status=204)
    except IndexError:
        return Response('Not Found', status=404)


@people.route('/<int:id>/posts')
def get_person_post(id):
    db_content = get_db()
    list_ = [p for p in db_content['posts'] if p['userId'] == id]

    return jsonify(list_) if list_ else Response('Not Found', status=404)


@people.route("/<name>")
def get_name(name):
    return f"<h1>Hello, {name.title()}!</h1>"
