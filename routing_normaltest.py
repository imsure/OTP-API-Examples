"""
Issuing 1000 routing requests sequentially to OTP server, 200 for each city.
"""

import utils
import requests
from datetime import datetime

if __name__ == '__main__':
    total = 100
    reqs = []
    routers = []
    for name in utils.router_names:
        router = utils.routerInfo(name)
        routers.append(router)
        for i in range(0, int(total * 0.2)):
            url, payload = utils.makeTravelRequestByStop(router)
            reqs.append((url, payload))

    index = 1
    for req in reqs:
        tstart = datetime.now()
        ret = requests.get(req[0], params=req[1])
        tend = datetime.now()
        tdelta = tend - tstart
        json_obj = ret.json()
        iti_count = 0
        if 'plan' in json_obj and 'itineraries' in json_obj['plan']:
            iti_count = len(json_obj['plan']['itineraries'])
        print(index, ret.status_code, tdelta.microseconds/1e3, iti_count)
        index += 1
