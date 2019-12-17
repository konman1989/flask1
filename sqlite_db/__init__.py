from flask import Flask
from flask_restful import Api

from sqlite_db.routs import Posts, DetailedPosts, Comments, DetailedComments, \
    DetailedPostComments


app = Flask(__name__)
api = Api(app)

api.add_resource(Posts, '/posts')
api.add_resource(DetailedPosts, '/posts/<int:post_id>')
api.add_resource(Comments, '/comments')
api.add_resource(DetailedComments, '/comments/<int:comment_id>')
api.add_resource(DetailedPostComments, '/posts/<int:post_id>/comments')


if __name__ == '__main__':
    app.run(debug=True)

    # api.add_resource(Albums, '/albums')
    # api.add_resource(DetailedAlbums, '/albums/<int:album_id>')
    # api.add_resource(Users, '/users')
    # api.add_resource(DetailedUsers, '/users/<int:user_id>')
