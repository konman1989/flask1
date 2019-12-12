import json


def get_db():
    with open('data.json', 'r') as file_:
        return json.load(file_)


def update_db(content):
    with open('data.json', 'w') as file_:
        json.dump(content, file_, indent=2)
