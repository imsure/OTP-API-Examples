import utils
import requests
import json
import sys
from datetime import datetime
from requests_futures.sessions import FuturesSession # Asynchronous HTTP Requests

def bg_cb(sess, resp):
    # record the time the response was received
    resp.tend = datetime.now()

if __name__ == '__main__':
    total = 10
    reqs = []
    routers = []
    for name in utils.router_names:
        router = utils.routerInfo(name)
        routers.append(router)
        if name != 'tucson':
            for i in range(0, int(total * 0.3)):
                url, payload = utils.makeTravelRequestRandom(router)
                reqs.append((url, payload))
        else:
            for i in range(0, int(total * 0.1)):
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
        print (index, res.status_code, tdelta.microseconds/1e3)
        index += 1

    # print (len(reqs))
