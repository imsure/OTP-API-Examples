import requests
import json
import random
import sys
import math
from datetime import datetime
from random import randrange, randint
import conf
import zipfile
import glob
import pandas as pd
import pytz


router_names = ["tucson", "denver", "houston", "austin", "elpaso"]
modes = ['TRANSIT,WALK', 'TRANSIT,BICYCLE', 'WALK', 'BICYCLE']


class Router(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ('{}: lower left: ({}, {}), upper right: '
                '({}, {}), central: ({}, {})'
                ' # of stops: {}').format(self.name,
                                          self.lo_left_lat, self.lo_left_lon,
                                          self.up_right_lat, self.up_right_lon,
                                          self.central_lat, self.central_lon,
                                          len(self.stops))

    def stop_lat_lon(self, index):
        return self.stops['stop_lat'][index], self.stops['stop_lon'][index]


def extractStops(router_name):
    fname = glob.glob('{}/{}.*.zip'.format(conf.gtfsPath, router_name))[0]
    f = zipfile.ZipFile(fname, 'r')
    df = pd.read_csv(f.open('stops.txt'))
    return df[['stop_lat', 'stop_lon']]


def routerInfo(router_name):
    url = "{}/otp/routers/{}".format(conf.ec2ip, router_name)
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

    router.stops = extractStops(router_name)

    return router


def randomGeoPoint(lat, lon, radius):
    r = radius/111300  # convert unit from meter to degree
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))

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
    return modes[randint(0, 3)]


def randomWalkDist():
    return random.uniform(804.672, 1609.34) # 0.5 mile - 1 mile


def currentDateTimeCentral():
    now_utc = datetime.now(pytz.timezone('UTC'))
    now_central = now_utc.astimezone(pytz.timezone('US/Central'))
    date = now_central.strftime('%m-%d-%y')

    hour = now_central.hour
    minute = now_central.minute
    suffix = 'am'
    if hour > 12:
        hour -= 12
        suffix = 'pm'
    elif hour == 12:
        suffix = 'pm'

    time = '{}:{}{}'.format(hour, str(minute).zfill(2), suffix)

    return date, time


def makeTravelRequestRandom(router):
    url = "{}/otp/routers/{}/plan".format(conf.ec2ip, router.name)

    radius = 30000  # meters
    from_lat, from_lon = randomGeoPoint(router.central_lat, router.central_lon, radius)
    to_lat, to_lon = randomGeoPoint(router.central_lat, router.central_lon, radius)

    date = datetime.today().strftime('%m-%d-%y')
    time = randomTime()
    mode = randomMode()
    max_walk = randomWalkDist()

    payload = {
        'fromPlace': '{},{}'.format(from_lat, from_lon),
        'toPlace': '{},{}'.format(to_lat, to_lon),
        'time': '{}'.format(time),
        'date': '{}'.format(date),
        'mode': '{}'.format(mode),
        'maxWalkDistance': '{}'.format(max_walk),
        'arriveBy': 'false',
        'wheelchair': 'false',
        'locale': 'en'
    }

    return url, payload


def makeTravelRequestByStop(router):
    url = "{}/otp/routers/{}/plan".format(conf.ec2ip, router.name)

    radius = 300  # meters
    indexes = random.sample(range(0, len(router.stops) - 1), 2)
    from_lat, from_lon = router.stop_lat_lon(indexes[0])
    from_lat, from_lon = randomGeoPoint(from_lat, from_lon, radius)
    to_lat, to_lon = router.stop_lat_lon(indexes[1])
    to_lat, to_lon = randomGeoPoint(to_lat, to_lon, radius)

    date, time = currentDateTimeCentral()
    mode = randomMode()
    max_walk = randomWalkDist()

    payload = {
        'fromPlace': '{},{}'.format(from_lat, from_lon),
        'toPlace': '{},{}'.format(to_lat, to_lon),
        'time': '{}'.format(time),
        'date': '{}'.format(date),
        'mode': '{}'.format(mode),
        'maxWalkDistance': '{}'.format(max_walk),
        'arriveBy': 'false',
        'wheelchair': 'false',
        'locale': 'en'
    }

    return url, payload


if __name__ == '__main__':
    # date, time = currentDateTimeCentral()
    # print(date)
    # print(time)

    routers = []
    for name in router_names:
        router = routerInfo(name)
        routers.append(router)
        lat, lon = router.stop_lat_lon(0)
        # print(lat, lon)
        # print(router)
        # url, payload = makeTravelRequestByStop(router)
        url, payload = makeTravelRequestRandom(router)
        ret = requests.get(url, params=payload)
        # print(ret.text)
        json_obj = ret.json()
        iti_count = 0
        if 'plan' in json_obj and 'itineraries' in json_obj['plan']:
            iti_count = len(json_obj['plan']['itineraries'])

        print('router: {}; status: {}; # of itineraries: {}'.format(router.name,
                                                                    ret.status_code,
                                                                    iti_count))

    exit(0)
