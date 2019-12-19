import sqlite3


def get_db(table_name):

    """Returns all DB values. Can be used for any DB with a given DB name"""

    with sqlite3.connect('db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        users = curs.execute(f"select * from {table_name}")
        return users


def get_user_comments(user_id):
    with sqlite3.connect('db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        t = (user_id,)
        comments = curs.execute('''select * from comments where user_id=?''', t)

        # comments = curs.execute('''select * from users join comments on
        # users.id = comments.user_id where user_id=?''', t)
        return comments


def get_post_comments(post_id):
    with sqlite3.connect('db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        t = (post_id,)
        comments = curs.execute('''select * from comments where user_id=?''', t)
        return comments


def get_user_stats():
    with sqlite3.connect('db.db') as conn:
        curs = conn.cursor()
        curs.execute('''select name, count(name) from users 
        join comments on
        users.id=comments.user_id 
        group by name 
        order by count(comments.id) desc''')
        return dict(curs.fetchall())


def get_text_inside(text):
    with sqlite3.connect('db.db') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        t = (f"%{text}%",)
        curs.execute(
            '''select * from posts where data like ?''', t)
        return curs




