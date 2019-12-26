from datetime import datetime
from sqlalchemy_1.settings import db

subscriptions = db.Table('subscriptions',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('message_id', db.Integer,
                                   db.ForeignKey('message.id')),
                         db.Column('room_id', db.Integer,
                                   db.ForeignKey('room.id'))
                         )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    avatar = db.Column(db.String(50), unique=False, nullable=True,
                       default='default.jpg')
    rooms = db.relationship('Room', secondary=subscriptions,
                            backref=db.backref('subscribers', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "country": self.country,
            "avatar": self.avatar,
        }


class Message(db.Model):
    __tablename_ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer,
                          db.ForeignKey("user.id"),
                          nullable=False)
    receiver_id = db.Column(db.Integer,
                            db.ForeignKey("user.id"),
                            nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    sender = db.relationship("User", foreign_keys=[sender_id])
    receiver = db.relationship("User", foreign_keys=[receiver_id])
    rooms = db.relationship('Room', secondary=subscriptions,
                            backref=db.backref('messages', lazy='dynamic'))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S")
        }

    def __repr__(self):
        return f"{self.id}"


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.strftime("%d-%m-%Y %H:%M:%S"),
        }

    def __repr__(self):
        return f"{self.id}, {self.name}, " \
               f"{self.created_at.strftime('%d-%m-%Y %H:%M:%S')}"


if __name__ == '__main__':
    db.create_all()
