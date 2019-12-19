from flask import Flask
from flask_restful import Api

from database.routs_class import Users, DetailedPostComments, \
    DetaledUserComments, UserStats, Posts, Comments, PostsSearch

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(DetaledUserComments, '/users/<int:user_id>/comments')
api.add_resource(DetailedPostComments, '/posts/<int:post_id>/comments')
api.add_resource(Posts, '/posts')
api.add_resource(PostsSearch, '/posts/search')
api.add_resource(Comments, '/comments')
api.add_resource(UserStats, '/users/stats')

if __name__ == '__main__':
    app.run(debug=True)







