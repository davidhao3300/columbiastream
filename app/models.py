from hashlib import md5
from app import db
from app import app
from config import WHOOSH_ENABLED
import re
import time
import api

ROLE_USER = 0
ROLE_ADMIN = 1

class Bet(db.Model):
    __tablename__ = 'bets'
    better_id = db.Column(db.Integer, db.ForeignKey('better.id'), primary_key=True)
    pic_id = db.Column(db.String, db.ForeignKey('pic.id'), primary_key=True)
    end_time = db.Column('end_time', db.Integer)
    amount = db.Column('amount', db.Integer)
    pic = db.relationship("Post", backref = "bet")
    expired = db.Column("expired", db.Boolean, default = False)
    result = db.Column("result", db.Integer)
    new = db.Column("new", db.Boolean, default = False)
    payout = db.Column("payout", db.Integer)
    money = db.Column("money", db.Integer, default = 100)
    
    def  __repr__(self):
        return "<Bet %r - %r, end: %r, amount: %r, expired: %r, result: %r>" % (self.pic, self.better, self.end_time, self.amount, self.expired, self.result)

    def dict_version(self):
        return {"better" : self.better.dict_version(), "pic" : self.pic.dict_version(), "end_time" : self.end_time, "amount" : self.amount,
                "expired" : self.expired, "result" :self.result, "payout" : self.payout, "money" : self.money, "new" : self.new}

    def dict_version_self(self):
        return {"pic" : self.pic.dict_version(), "end_time" : self.end_time, "amount" : self.amount, "expired" : self.expired, "result" : self.result}

    @staticmethod
    def min_time():
        return min_time

    def new_min_time():
        min_time = sorted(Bet.query.filter_by(expired = False).all(), key=lambda bet : bet.end_time)[0].end_time

class User(db.Model):
    __tablename__ = "better"
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(64))
    profile_pic = db.Column(db.String(100), index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    username = db.Column(db.String(64), unique = True)
    about = db.Column(db.String(300))
    website = db.Column(db.String(120))
    access_token = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    betted = db.relationship("Bet", backref = "better")
    currency = db.Column(db.Integer())
    
    def bet(self, picture, bet_amount, bet_time):
        if not self.has_betted(picture):
            bet = Bet(end_time = bet_time + int(time.time()), amount =bet_amount, money = 100)
            bet.pic = picture
            self.betted.append(bet)
            print self.currency, bet.money
            self.currency -= bet.money
            db.session.add(self)
            db.session.commit()
            return self

    def update(self):
        bets = self.betted
        for bet in bets:
            pic_id = bet.pic.id


    def has_betted(self, picture):
        return Bet.query.filter_by(better_id = self.id, pic_id = picture.id).count() > 0

    def current_bets(self):
        bets = Bet.query.filter_by(better_id = self.id).order_by("end_time desc").all()
        return bets

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return profile_pic

    def __repr__(self): # pragma: no cover
        return '<User %r>' % (self.username)    

    def dict_version(self):
        return {"id" : self.id,
                "fullname" : self.fullname,
                "username" : self.username,
                "profile_pic" : self.profile_pic,
                "about" : self.about,
                "website" : self.website,
                "folowers" : self.followers,
                "currency" : self.currency
        }
        
class Post(db.Model):
    __tablename__ = "pic"
    id = db.Column(db.String(100), primary_key = True)
    link = db.Column(db.String(140))
    small_link = db.Column(db.String(140))
    timestamp = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    poster = db.Column(db.Integer)

    def get_betters(self):
        return self.betters.order_by(User.username.asc()).all()

    def __repr__(self): # pragma: no cover
        return '<Post %r>' % (self.link)

    def dict_version(self):
        return {"id" : self.id,
                "link" : self.link,
                "small_link" : self.small_link,
                "timestamp" : self.timestamp,
                "likes" : self.likes,
                "poster" : self.poster
        }
