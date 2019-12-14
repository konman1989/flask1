from flask import request, jsonify, Response
from flask_restful import Resource
from typicode_copy.db_methods import get_db


class Posts(Resource):

    def get(self):
        db = get_db()
        args = request.args.get('userId')
        if args is not None:
            comments = [c for c in db['albums'] if c['userId'] == int(args)]
            return jsonify(comments) if comments else Response('Not Found',
                                                               status=404)
        return db['posts']

    def post(self):
        args = request.get_json()
        db = get_db()
        id_ = len(db['posts']) + 1
        db['posts'].append({'id': id_, **args})

        return {'id': id_}, 201


class DetailedPosts(Resource):

    def get(self, post_id):
        db = get_db()
        try:
            return jsonify(db['posts'][post_id - 1])
        except IndexError:
            return 'Not Found', 404

    def put(self, post_id):
        post = request.get_json()
        db = get_db()

        try:
            db['posts'][post_id - 1] = post
            print(db['posts'][post_id - 1])
            return {}, 204
        except IndexError:
            return 'Not found', 404

    def patch(self, post_id):
        post = request.get_json()
        db = get_db()

        try:
            db['posts'][post_id - 1].update(post)
            return {}, 204

        except IndexError:
            return 'Not found', 404

    def delete(self, post_id):
        db = get_db()

        try:
            del db['posts'][post_id - 1]
            return {}, 204
        except IndexError:
            return 'Not found', 404


class Comments(Resource):

    def get(self):
        db = get_db()
        args = request.args.get('postId')
        if args is not None:
            comments = [c for c in db['comments'] if c['postId'] == int(args)]
            return jsonify(comments) if comments else Response('Not Found',
                                                               status=404)
        return db['comments']


class DetailedComments(Resource):

    def get(self, post_id):
        db = get_db()
        comments = [c for c in db['comments'] if c['postId'] == int(post_id)]
        return jsonify(comments) if comments else Response('Not Found',
                                                           status=404)


class Albums(Resource):

    def get(self):
        db = get_db()
        args = request.args.get('userId')
        if args is not None:
            albums = [a for a in db['albums'] if
                      a['userId'] == int(args)]
            return jsonify(albums) if albums else Response('Not Found',
                                                           status=404)
        return db['albums']

    def post(self):
        args = request.get_json()
        db = get_db()
        id_ = len(db['albums']) + 1
        db['albums'].append({'id': id_, **args})

        return {'id': id_}, 201


class DetailedAlbums(Resource):
    def get(self, album_id):
        db = get_db()
        try:
            return jsonify(db['albums'][album_id - 1])
        except IndexError:
            return 'Not found', 404


class Users(Resource):
    def get(self):
        db = get_db()
        args = request.args.get('id')
        if args is not None:
            users = [a for a in db['users'] if
                     a['id'] == int(args)]
            return jsonify(users) if users else Response('Not Found',
                                                         status=404)
        return db['users']


class DetailedUsers(Resource):
    def get(self, user_id):
        db = get_db()
        try:
            return jsonify(db['users'][user_id - 1])
        except IndexError:
            return 'Not found', 404
