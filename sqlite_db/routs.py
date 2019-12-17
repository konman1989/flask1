from flask import request, Response
from flask_restful import Resource
from sqlite_db.api import get_db, get_db_by_id, post_db, delete_db_item, \
    put_db, patch_db, get_comments_to_post


class Posts(Resource):

    def get(self):
        args = request.args.get('userId')

        if args is not None:
            db = [dict(post) for post in get_db('posts')
                  if dict(post)['userId'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('posts')]

    def post(self):
        args = request.get_json()

        try:
            post_id = post_db(**args)
            return post_id, 201
        except TypeError:
            return "Wrong input", 404


class DetailedPosts(Resource):

    def get(self, post_id):
        try:
            return get_db_by_id(post_id, 'posts')
        except TypeError:
            return "Not found", 404

    def put(self, post_id):
        args = request.get_json()

        try:
            put_db(post_id, **args)
            return {}, 204
        except IndexError:
            return 'Not found', 404

    def patch(self, post_id):
        args = request.get_json()

        try:
            if patch_db(post_id, **args) is False:
                return 'Wrong keyword, check your input', 404
            return {}, 204
        except TypeError:
            return 'Not found', 404

    def delete(self, post_id):
        result = delete_db_item(post_id)

        if result == 1:
            return {}, 204
        else:
            return 'Not found', 404


class Comments(Resource):

    def get(self):
        args = request.args.get('postId')

        if args is not None:
            db = [dict(post) for post in get_db('comments')
                  if dict(post)['postId'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('comments')]


class DetailedComments(Resource):

    def get(self, comment_id):
        try:
            return get_db_by_id(comment_id, 'comments')
        except TypeError:
            return "Not found", 404


class DetailedPostComments(Resource):

    def get(self, post_id):
        list_ = [dict(post) for post in get_comments_to_post(post_id)]
        return list_ if list_ else "Not found", 404




