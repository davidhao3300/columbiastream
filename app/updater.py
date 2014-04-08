from time import time, sleep
from threading import Timer, Thread
from models import Bet
from app import db
import api

min_time = 0
x = 0
access_token = "1050839566.532a562.07583b2aa71c44039e8e490e940b8a65"

def startTimer():
        global x
        if x != 0:
                return False
        thr = Thread(target = loopTimer)
        thr.start()
        x += 1
        return True

def loopTimer():
        global min_time
        while True:
                bets = Bet.query.filter_by(expired = False).order_by("end_time asc").all()
                if len(bets) > 0:
                        min_time = bets[0].end_time
                        while int(time()) >= min_time:
                                update(min_time)
                        print min_time, int(time())
                #sleep(min(min_time - int(time()), 60*60))
                sleep(1)


def update(the_min_time):
        global min_time
        bets = Bet.query.filter_by(expired = False).order_by("end_time asc").all()
        index = 0
        for i in range(len(bets)):
                bet = bets[i]
                if bet.end_time <= int(time()):
                        bet.expired = True
                        bet.new = True
                        photo_data = api.pic_info(bet.pic.id, access_token)
                        bet.result = photo_data["likes"]["count"]
                        user_info = api.user_info(bet.pic.poster, access_token)
                        average_info = api.average(bet.pic.poster, access_token)
                        bet.payout = bet.money * calc_payout(bet.amount, 100 * bet.result / float(user_info["counts"]["followed_by"]), average_info["percentage"])
                        bet.better.currency += bet.payout
                        print bet.payout
                        db.session.commit()
                else: 
                        index = i
                        break
        if index == len(bets):
                min_time = 0
        else:
                min_time = bets[index].end_time

def calc_payout(bet_percent, actual_percent, average_percent):
        base = 0
        if actual_percent <= average_percent and bet_percent <= average_percent:
                base = 1
        elif actual_percent >= average_percent and bet_percent >= average_percent:
                base = 1
        diff = actual_percent - bet_percent
        if diff < -5 or diff > 10:
                return 0+base
        if diff < 1 and diff > -1:
                return 10+base
        if diff <= -1:
                return int(2 + 0.4 * diff)+base
        else:
                return int(2 - 0.2 * diff)+base