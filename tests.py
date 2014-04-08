#!flask/bin/python
import os
import unittest
import time
from config import basedir
from app import app, db
from app.models import User, Post, Bet
import app.updater as updater


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()
        updater.startTimer()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_bet(self):
        u1= User(id = 123, username = 'john', fullname = "John Doe", profile_pic = "fake.jpg", website = "", about = "", access_token = "not")
        u2 = User(id = 456, username = 'billy', fullname = "Billy Doe", profile_pic = "fake.jpg", website = "", about = "", access_token = "not")
        u3= User(id = 123, username = 'john', fullname = "John Doe", profile_pic = "fake.jpg", website = "", about = "", access_token = "not")
        p1 = Post(id = "2_2", link = "fake3.jpg", timestamp = 12412, likes = 123)
        p2 = Post(id = "3_2", link = "fake4.jpg", timestamp = 346821, likes = 12421)

        u1.bet(p1, 1248, 123)
        u1.bet(p2, 82359, 10)
        u1.bet(p1, 1249, 128941820)
        u2.bet(p2, 3946890, 58295)
        db.session.commit()
        #print User.query.filter_by(id=u1.id).all()
        #print Post.query.all()
        #print sorted(Bet.query.all(), key=lambda bet : bet.end_time)
        print Bet.query.order_by("end_time asc").all()
        time.sleep(20)
        print Bet.query.order_by("end_time asc").all()

if __name__ == '__main__':
    unittest.main()