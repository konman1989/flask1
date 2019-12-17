import sqlite3
import requests
from bs4 import BeautifulSoup


def create_fake_dictionary(url: str) -> dict:

    """Parsing links to create a fake DB and creates a dict"""

    data = requests.get(url).content
    soup = BeautifulSoup(data, 'html.parser')
    div = soup.find('table')

    db = {}
    for link in div.find_all('a'):
        db[link['href'][1:]] = requests.get(f"{url}{link['href'][1:]}").json()

    return db


def create_db_table_posts():

    """Creates one table out of dict by one of its keys: posts.
    Name can be any string"""

    with sqlite3.connect('fake_db.db') as conn:
        conn.execute('''create table posts ( 
                  id integer unique primary key autoincrement, 
                  userId integer not null, 
                  title varchar(100) not null, 
                  body varchar not null 
            )''')

        dict_ = create_fake_dictionary('https://jsonplaceholder.typicode.com/')

        for item in dict_['posts']:
            t = (item['userId'], item['title'], item['body'], )
            conn.execute('''insert into posts (userId, title, body)
            values (?, ?, ?)''', t)


def create_db_table_comments():

    """Creates one table out of dict by one of its keys: comments.
    Name can be any string"""

    with sqlite3.connect('fake_db.db') as conn:
        conn.execute('''create table comments ( 
                  id integer unique primary key autoincrement, 
                  postId integer not null, 
                  name varchar(100) not null, 
                  email varchar(25) not null, 
                  body varchar not null 
            )''')

        dict_ = create_fake_dictionary('https://jsonplaceholder.typicode.com/')

        for item in dict_['comments']:
            t = (item['postId'], item['name'], item['email'], item['body'], )
            conn.execute('''insert into comments (postId, name, email, body)
            values (?, ?, ?, ?)''', t)


def get_db(table_name):

    """Returns all DB values. Can be used for any DB with a given DB name"""

    with sqlite3.connect('fake_db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        posts = curs.execute(f"select * from {table_name}")
        return posts


def get_db_by_id(item_id, table_name):

    """Returns value by its id. Can be used for any DB with a given DB name"""

    with sqlite3.connect("fake_db.db") as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        t = (item_id,)
        item = curs.execute(f"select * from {table_name} where id=?", t)
        return dict(item.fetchone())


def post_db(userId, title, body):
    with sqlite3.connect('fake_db.db') as conn:
        curs = conn.cursor()
        t = (userId, title, body)
        curs.execute(
            '''insert into
            posts(userId, title, body)
            values (?, ?, ?)''',
            t)
        return curs.lastrowid


def put_db(post_id, userId, title, body):
    with sqlite3.connect('fake_db.db') as conn:
        curs = conn.cursor()
        t = (userId, title, body, post_id)
        curs.execute('''update posts 
                        set userId=?, title=?, body=? where id=?''', t)


def patch_db(post_id, **args):
    # fetching and updating data
    row_to_update = get_post(post_id)
    row_to_update.update(**args)
    # deleting 'id' item to update db correctly
    del row_to_update['id']

    with sqlite3.connect('fake_db.db') as conn:
        curs = conn.cursor()
        t = (*row_to_update.values(), post_id)

        try:
            curs.execute('''update posts 
                            set userId=?, title=?, body=? where id=?''', t)
        except sqlite3.ProgrammingError:
            return False


def delete_db_item(post_id):
    with sqlite3.connect('fake_db.db') as conn:
        curs = conn.cursor()
        t = (post_id,)
        curs.execute('''delete from posts where id=?''', t)
        return curs.rowcount


def get_comments_to_post(post_id):
    with sqlite3.connect('fake_db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        t = (post_id,)
        comments = curs.execute('''select * from comments join posts on
        comments.postId = posts.id where postId=?''', t)
        return comments


if __name__ == '__main__':
    conn = sqlite3.connect('fake_db.db')
    # create_db_table_posts()
    # create_db_table_comments()


