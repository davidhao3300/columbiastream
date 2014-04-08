import urllib2
import json
import datetime
import urllib

base_url = "https://api.instagram.com/"
client_id = "532a5629d03141ab929812cff97d0c00"
client_secret = "9fd45504ab6a442abfa2425dc0932ee4"
min_time = 0

def login(code):
        url = base_url + "oauth/access_token"
        values = {"client_id":client_id, 
        "client_secret" : client_secret, 
        "grant_type" : "authorization_code", 
        "code":code, 
        "redirect_uri":"http://socialbookie.herokuapp.com/login"
        }
        values = urllib.urlencode(values)
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        if "error_type" in data:
                return None
        data2 = user_info(int(data["user"]["id"]), data["access_token"])
        return {"user" : data2, "access_token" : data["access_token"]}

def user_info(user_id, access_token):
        url = base_url + "v1/users/" + str(user_id) + "?access_token=" + access_token
        response = urllib2.urlopen(url)
        data = json.loads(response.read())["data"]
        return data

def feed(access_token):
        url = base_url + "v1/users/self/feed?access_token=" + access_token + "&count=50"
        print url
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        photos = filter(data["data"])
        while len(photos) < 50:
                new_url = base_url + "v1/users/self/feed?access_token=" + access_token + "&count=10"+ "&max_id=" + data["pagination"]["next_max_id"]
                print new_url
                response = urllib2.urlopen(new_url)
                data = json.loads(response.read())
                new_photos = filter(data["data"])
                photos.extend(new_photos)
        return photos

def filter(media):
        i = 0
        while i < len(media):
                if media[i]["type"] != "image":
                        media.pop(i)
                        i -= 1
                i += 1
        return media

def pic_info(pic_id, access_token):

        url = base_url + "v1/media/" + pic_id + "?access_token=" + access_token
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        return data["data"]

def recent(user_id, access_token):
        url = base_url + "v1/users/" + str(user_id) +"/media/recent/?access_token=" + access_token
        print url
        response = urllib2.urlopen(url)
        data = json.loads(response.read())["data"]
        return data

def average(user_id, access_token):
        data = recent(user_id, access_token)
        total = 0
        for photo in data:
                total += photo["likes"]["count"]
        if len(data) == 0:
                average = 0
        else:
                average = total / len(data)
        total_followers = user_info(int(user_id), access_token)["counts"]["followed_by"]
        percentage = 100.0 * average / total_followers
        return {"average followers" : average, "percentage" : percentage, "total followers" : total_followers}
