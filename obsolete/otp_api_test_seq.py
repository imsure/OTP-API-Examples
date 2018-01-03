import utils as utils
import requests
import json
import sys
from datetime import datetime
from requests_futures.sessions import FuturesSession # Asynchronous HTTP Requests

if __name__ == '__main__':
    total = 1000
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

    for req in reqs:
        tstart = datetime.now()
        ret = requests.get(req[0], params=req[1])
        tend = datetime.now()
        tdelta = tend - tstart
        print (ret.status_code, tdelta.microseconds/1e3)

    # # max workers set to 10, default is 2
    # session = FuturesSession(max_workers=10)
    # futures = []
    # for req in reqs:
    #     tstart = datetime.now()
    #     f = session.get(req[0], params=req[1])
    #     futures.append((f, tstart))

    # # wait for requests to complete
    # index = 1
    # for f in futures:
    #     res = f[0].result()
    #     tend = datetime.now()
    #     tdelta = tend - f[1]
    #     print (index, res.status_code, tdelta.microseconds/1e3)
    #     index += 1

    # print (len(reqs))
