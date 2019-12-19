from flask import request, Response
from flask_restful import Resource
from database.api import get_db, get_user_comments, get_post_comments, \
    get_user_stats, get_text_inside


class Users(Resource):
    def get(self):
        args = request.args.get('user_id')

        if args is not None:
            db = [dict(post) for post in get_db('users')
                  if dict(post)['id'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('users')]


class DetaledUserComments(Resource):

    def get(self, user_id):
        list_ = [dict(post) for post in get_user_comments(user_id)]
        return list_ if list_ else "Not found", 404


class DetailedPostComments(Resource):

    def get(self, post_id):
        list_ = [dict(post) for post in get_post_comments(post_id)]
        return list_ if list_ else "Not found", 404


class Posts(Resource):

    def get(self):
        args = request.args.get('post_id')

        if args is not None:
            db = [dict(post) for post in get_db('posts')
                  if dict(post)['id'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('posts')]


class PostsSearch(Resource):

    def get(self):
        args = request.args.get('query')

        if args is not None:
            db = [dict(post) for post in get_text_inside(args)]
            return db if db else Response, 404


class Comments(Resource):

    def get(self):
        args = request.args.get('comment_id')

        if args is not None:
            db = [dict(post) for post in get_db('comments')
                  if dict(post)['id'] == int(args)]
            return db if db else Response('Not Found', status=404)
        return [dict(post) for post in get_db('comments')]


class UserStats(Resource):

    def get(self):
        return get_user_stats()










