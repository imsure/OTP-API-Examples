"""
Testing methodology:
- issuing total 1000 routing requests to 5 cities from two hosts
  (one from Metropia office, one from EC2 instance at US West) at the same time,
  each is responsible of 500 requests.
- Each host utilizes 10 threads to send out 500 requests concurrently
- For each 500 requests, 400 of them are issued by picking up locations around know stops,
  while 100 of them are issued completely randomly.
"""

import utils
import requests
import json
import sys
from datetime import datetime
from requests_futures.sessions import FuturesSession  # Asynchronous HTTP Requests


# session callback
def bg_cb(sess, resp):
    # record the time the response was received
    resp.tend = datetime.now()


if __name__ == '__main__':
    total = 500
    reqs = []
    routers = []
    for name in utils.router_names:
        router = utils.routerInfo(name)
        routers.append(router)

        # 5 cities(routers), each got 20% requests
        city_total = int(total * 0.2)
        for i in range(0, int(city_total * 0.8)): # 80% are very likely to get valid trip plans
            url, payload = utils.makeTravelRequestByStop(router)
            reqs.append((url, payload))

        for i in range(0, int(city_total * 0.2)):  # 20% are less possible to get any valid trip plans
            url, payload = utils.makeTravelRequestRandom(router)
            reqs.append((url, payload))

    # max workers set to 10, default is 2
    session = FuturesSession(max_workers=10)
    futures = []
    for req in reqs:
        tstart = datetime.now()
        f = session.get(req[0], params=req[1], background_callback=bg_cb)
        futures.append((f, tstart))

    # wait for requests to complete
    index = 1
    for f in futures:
        res = f[0].result()
        tstart = f[1]
        tdelta = res.tend - tstart
        json_obj = res.json()
        iti_count = 0
        if 'plan' in json_obj and 'itineraries' in json_obj['plan']:
            iti_count = len(json_obj['plan']['itineraries'])
        print(index, res.status_code, tdelta.microseconds/1e3, iti_count)
        index += 1

    # print(len(reqs))
