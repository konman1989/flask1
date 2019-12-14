from flask import Flask
from flask_restful import Api

from typicode_copy.routs import Posts, DetailedPosts, Comments, \
    DetailedComments, Albums, DetailedAlbums, Users, DetailedUsers

app = Flask(__name__)
api = Api(app)

api.add_resource(Posts, '/posts')
api.add_resource(DetailedPosts, '/posts/<int:post_id>')
api.add_resource(Comments, '/comments')
api.add_resource(DetailedComments, '/posts/<int:post_id>/comments')
api.add_resource(Albums, '/albums')
api.add_resource(DetailedAlbums, '/albums/<int:album_id>')
api.add_resource(Users, '/users')
api.add_resource(DetailedUsers, '/users/<int:user_id>')


if __name__ == '__main__':
    app.run(debug=True)
