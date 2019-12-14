from flask import Blueprint, Response, jsonify, request
from db_methods import get_db, update_db


posts = Blueprint('posts', __name__)


@posts.route('/')
def get_posts():
    user_id = (request.args.get('user_id'))
    db_content = get_db()

    if user_id is not None:
        list_ = [p for p in db_content['posts'] if p['userId'] == int(user_id)]

        return jsonify(list_) if list_ else Response('Not Found', status=404)
    return jsonify(db_content['posts'])


@posts.route('/', methods=['POST'])
def post_post():
    post = request.get_json()
    db_content = get_db()

    max_id = max([p['id'] for p in db_content['posts']])
    post_id = max_id + 1

    db_content['posts'].append({'id': post_id, **post})
    update_db(db_content)
    return jsonify({'id': post_id}), 201


@posts.route('/<int:id>')
def get_post(id):
    db_content = get_db()

    list_ = [p for p in db_content['posts'] if p['id'] == id]
    return jsonify(list_) if list_ else Response('Not Found', status=404)


@posts.route('/<int:id>', methods=['DELETE'])
def delete_post(id):
    db_content = get_db()
    try:
        item_to_delete = [p for p in db_content['posts'] if p['id'] == id]
        db_content['posts'].remove(item_to_delete[0])
        update_db(db_content)

        return Response(status=204)
    except IndexError:
        return Response('Not Found', status=404)


@posts.route('/<int:id>', methods=['PATCH'])
def update_post(id):
    db_content = get_db()
    try:
        item_to_update = [p for p in db_content['posts'] if p['id'] == id]
        index_to_update = db_content['posts'].index(item_to_update[0])
        db_content['posts'][index_to_update].update(request.get_json())
        update_db(db_content)

        return Response(status=204)
    except IndexError:
        return Response('Not Found', status=404)

