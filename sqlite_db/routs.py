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
            return post_db('posts', **args)
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
            return put_db('posts', post_id, **args)
        except IndexError:
            return 'Not found', 404

    def patch(self, post_id):
        args = request.get_json()

        try:
            return patch_db('posts', post_id, **args)
        except TypeError:
            return 'Not found', 404

    def delete(self, post_id):
        return delete_db_item('posts', post_id)


class Comments(Resource):

    def get(self):
        args = request.args.get('postId')

        if args is not None:
            db = [dict(post) for post in get_db('comments')
                  if dict(post)['postId'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('comments')]

    def post(self):
        args = request.get_json()

        try:
            return post_db('comments', **args)
        except TypeError:
            return "Wrong input", 404


class DetailedComments(Resource):

    def get(self, comment_id):
        try:
            return get_db_by_id(comment_id, 'comments')
        except TypeError:
            return "Not found", 404

    def put(self, comment_id):
        args = request.get_json()

        try:
            return put_db('comments', comment_id, **args)
        except IndexError:
            return 'Not found', 404

    def patch(self, comment_id):
        args = request.get_json()

        try:
            return patch_db('comments', comment_id, **args)
        except TypeError:
            return 'Not found', 404

    def delete(self, comment_id):
        return delete_db_item('comments', comment_id)


class DetailedPostComments(Resource):

    def get(self, post_id):
        list_ = [dict(post) for post in get_comments_to_post(post_id)]
        return list_ if list_ else "Not found", 404




