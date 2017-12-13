import requests
import json
import random
import sys
import math
import datetime
from random import randrange, randint

ec2ip = "http://34.212.174.108:8080"
router_names = ["pdx", "houston", "austin", "tucson"]
radius = 20000 # meters
modes = ['TRANSIT,WALK', 'TRANSIT,BICYCLE', 'WALK', 'BICYCLE']

class Router(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ('router {}: lower left: ({}, {}), upper right: '
                '({}, {}), central: ({}, {})').format(self.name,
                                                      self.lo_left_lat, self.lo_left_lon,
                                                      self.up_right_lat, self.up_right_lon,
                                                      self.central_lat, self.central_lon)


def routerInfo(router_name):
    url = "{}/otp/routers/{}".format(ec2ip, router_name)
    # print (url)
    ret = requests.get(url)
    # print (ret.status_code)
    json_obj = ret.json()
    router = Router(router_name)
    router.lo_left_lat = json_obj['lowerLeftLatitude']
    router.lo_left_lon = json_obj['lowerLeftLongitude']
    router.up_right_lat = json_obj['upperRightLatitude']
    router.up_right_lon = json_obj['upperRightLongitude']
    router.central_lat = (router.lo_left_lat + router.up_right_lat) / 2
    router.central_lon = (router.lo_left_lon + router.up_right_lon) / 2

    return router


def randomGeoPoint(lat, lon):
    r = radius/111300
    u = float(random.uniform(0.0,1.0))
    v = float(random.uniform(0.0,1.0))

    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)

    return (lat + x, lon + y)


def randomDate():
    day = randrange(1,30)
    time = randrange(1,12)
    ampm = ''
    if randint(0, 1):
        ampm = 'am'
    else:
        ampm = 'pm'
    return '12-{}-2017'.format(day)


def randomTime():
    hour = randrange(1,12)
    minute = randrange(10,59)
    ampm = ''
    if randint(0, 1):
        ampm = 'am'
    else:
        ampm = 'pm'
    return '{}:{}{}'.format(hour, minute, ampm)


def randomMode():
    return modes[randint(0,3)]


def randomWalkDist():
    return random.uniform(804.672, 1609.34) # 0.5 mile - 1 mile


def makeTravelRequest(router):
    url = "{}/otp/routers/{}/plan".format(ec2ip, router.name)
    from_lat, from_lon = randomGeoPoint(router.central_lat, router.central_lon)
    to_lat, to_lon = randomGeoPoint(router.central_lat, router.central_lon)
    date = randomDate()
    time = randomTime()
    mode = randomMode()
    max_walk = randomWalkDist()
    payload = {'fromPlace': '{},{}'.format(from_lat, from_lon),
               'toPlace': '{},{}'.format(to_lat, to_lon),
               'time': '{}'.format(time),
               'date': '{}'.format(date),
               'mode': '{}'.format(mode),
               'maxWalkDistance': '{}'.format(max_walk),
               'arriveBy': 'false',
               'wheelchair': 'false',
               'locale': 'en'}

    return url, payload


if __name__ == '__main__':
    routers = []
    for name in router_names:
        router = routerInfo(name)
        routers.append(router)

    # for router in routers:
      #  print (router)

    router = routers[2]
    print (router)
    for i in range(1, 10):
        # print (randomGeoPoint(router.central_lat, router.central_lon))
        # print (randomDate())
        # print (randomTime())
        # print (randomMode())
        url, payload = makeTravelRequest(router)
        ret = requests.get(url, params=payload)
        print (ret.url)
        print (ret.status_code)
