from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy_1.settings import app, db, api
from sqlalchemy_1.models import User, Message, Room


class Users(Resource):

    def get(self):
        return [u.serialize() for u in User.query.all()], 200

    def post(self):
        try:
            data = request.get_json()
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return {'id': user.id}, 201
        except TypeError:
            return 'Wrong input', 404
        except IntegrityError:
            return 'Wrong input', 404


api.add_resource(Users, '/users')


class DetailedUser(Resource):

    def get(self, user_id):
        try:
            return User.query.get(user_id).serialize(), 200
        except AttributeError:
            return 'Not found', 404

        # return [u.serialize() for u in User.query.all()
        #         if u.serialize()["id"] == user_id], 200

    def patch(self, user_id):
        data = request.get_json()
        db.session.query(User).filter_by(id=user_id).update(data)
        db.session.commit()

        return {}, 204

    def delete(self, user_id):
        db.session.query(User).filter_by(id=user_id).delete()
        db.session.commit()

        return {}, 200


api.add_resource(DetailedUser, '/users/<int:user_id>')


class UserMessages(Resource):
    """Returns sent/received messages count"""

    def get(self, user_id):
        args = request.args.get('query')

        if args == 'sent':
            return db.session.query(Message).filter_by(
                sender_id=user_id).count()
        if args == 'received':
            return db.session.query(Message).filter_by(
                receiver_id=user_id).count()


api.add_resource(UserMessages, '/users/<int:user_id>/messages')


class Messages(Resource):

    def get(self):
        args_sender = request.args.get('sender_id')
        args_receiver = request.args.get('receiver_id')

        if args_receiver and args_receiver is not None:
            return [m.serialize() for m in
                    db.session.query(Message).filter_by(
                        sender_id=args_sender,
                        receiver_id=args_receiver
                    )]

        return [m.serialize() for m in db.session.query(Message).all()]

    def post(self):
        data = request.get_json()
        try:
            message = Message(**data)
            db.session.add(message)
            db.session.commit()
            return {'id': message.id}, 201
        except TypeError:
            return 'Wrong input', 400
        except IntegrityError:
            return 'Wrong input', 404


api.add_resource(Messages, '/messages')


class DetailedMessages(Resource):

    def get(self, message_id):
        try:
            return Message.query.get(message_id).serialize(), 200
        except AttributeError:
            return "Not found", 404

    def patch(self, message_id):
        data = request.get_json()

        # making sure send and receiver id match
        db.session.query(Message).filter_by(
            id=message_id,
            sender_id=data.get("sender_id"),
            receiver_id=data.get("receiver_id")
        ).update(data)
        db.session.commit()

        return {}, 204

    def delete(self, message_id):
        db.session.query(Message).filter_by(id=message_id).delete()
        db.session.commit()

        return {}, 200


api.add_resource(DetailedMessages, '/messages/<int:message_id>')


class Rooms(Resource):

    def get(self):
        return [r.serialize() for r in Room.query.all()], 200

    def post(self):
        data = request.get_json()
        try:
            room = Room(**data)
            db.session.add(room)
            db.session.commit()
            return {"id": room.id}, 201
        except TypeError:
            return 'Wrong input', 400
        except IntegrityError:
            return 'Wrong input', 404


api.add_resource(Rooms, '/rooms')


class RoomsDetailed(Resource):

    def get(self, room_id):
        try:
            return Room.query.get(room_id).serialize(), 200
        except AttributeError:
            return "Not found", 404

    def patch(self, room_id):
        data = request.get_json()
        db.session.query(Room).filter_by(id=room_id).update(data)
        db.session.commit()

        return {}, 204

    def delete(self, room_id):
        db.session.query(Room).filter_by(id=room_id).delete()
        db.session.commit()

        return {}, 200


api.add_resource(RoomsDetailed, '/rooms/<int:room_id>')


class RoomsUsers(Resource):

    def get(self, room_id):
        room = Room.query.get(room_id)
        return [user.name for user in room.subscribers], 200

    def post(self, room_id):
        data = request.get_json()

        # selecting a room where to add user
        room = Room.query.get(room_id)

        user_id = data.get('user_id')
        user = User.query.get(user_id)
        room.subscribers.append(user)

        db.session.commit()

        return {}, 204


api.add_resource(RoomsUsers, '/rooms/<int:room_id>/users')


class RoomsMessages(Resource):

    def get(self, room_id):
        room = Room.query.get(room_id)

        return [(message.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                 message.text) for message in room.messages], 201

    def post(self, room_id):
        data = request.get_json()

        sender_id = data.get("sender_id")
        user = User.query.get(sender_id)

        # selecting a room where to add message
        room = Room.query.get(room_id)

        if user not in room.subscribers:
            return "User is not subscribed", 400

        # adding message to the room
        message = Message(**data)
        room.messages.append(message)

        db.session.commit()
        return {}, 204


api.add_resource(RoomsMessages, '/rooms/<int:room_id>/messages')

if __name__ == '__main__':
    app.run(debug=True)


