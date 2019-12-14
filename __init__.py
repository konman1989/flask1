from flask import Flask

from people.routs import people
from posts.routs import posts
from main import main

app = Flask(__name__)

app.register_blueprint(people, url_prefix='/people')
app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True)
