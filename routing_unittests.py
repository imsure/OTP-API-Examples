## The OTP Routing API is a RESTful web service that responds
## to journey planning requests with itineraries in a JSON or
## XML representation.

## API doc: http://dev.opentripplanner.org/apidoc

import requests
import json
from conf import ec2ip

routers = ["denver", "houston", "austin", "tucson", "elpaso"]

# all should return valid routing plan of public transit
router2pos = {
    'denver': {'from': '39.75907,-104.99724', 'to': '39.72650,-104.99145'},
    'austin': {'from': '30.2859758,-97.7404588', 'to': '30.2727757,-97.7522587'},
    'houston': {'from': '29.7180255,-95.4002109', 'to': '29.7199535,-95.3444274'},
    'elpaso': {'from': '31.76000, -106.49157', 'to': '31.75236, -106.47984'},
    # UofA -> Metropia office
    # 'tucson': {'from': '32.23114, -110.94548', 'to': '32.2866043,-110.9473657'},
    # UofA -> Downtown
    # 'tucson': {'from': '32.2315175,-110.9565735', 'to': '32.22188, -110.96612'},
    # within UofA: old main -> arizona health science library
    'tucson': {'from': '32.23204, -110.95497', 'to': '32.23967, -110.94680'},
    # Davis-Monthan Air Force Base -> Metropia office, 0 itinerary returned for public transit
    #'tucson': {'from': '32.1748743,-110.8936878', 'to': '32.2866043,-110.9473657'},
}


# Make a routing request of OTP server
def route(router):
    url = "{}/otp/routers/{}/plan".format(ec2ip, router)
    payload = {
        'fromPlace': '{}'.format(router2pos[router]['from']),
        'toPlace': '{}'.format(router2pos[router]['to']),
        'time': '8:30am',
        'date': '2-22-2018',
        # 'date': '2-02-18',
        'mode': 'TRANSIT,WALK',
        # 'mode': 'BICYCLE',
        # 'mode': 'WALK',
        'maxWalkDistance': '804.672',
        'arriveBy': 'false',
        'wheelchair': 'false',
        'locale': 'en',
    }

    ret = requests.get(url, params=payload)
    # print(ret.url)
    if ret.ok:
        # print(ret.url)
        print(ret.text)
        print(ret.status_code)
        json_obj = ret.json()
        # print(type(json_obj)) # dict
        if 'plan' in json_obj and 'itineraries' in json_obj['plan']:
            print('# of itineraries: {}'.format(len(json_obj['plan']['itineraries'])))
        else:
            print('# of itineraries: 0')
    else:
        print(ret.status_code)


if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        print('Usage: {} <name of router>'.format(argv[0]))
        exit(-1)

    route(argv[1])
