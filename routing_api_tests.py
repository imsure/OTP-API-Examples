## The OTP Routing API is a RESTful web service that responds
## to journey planning requests with itineraries in a JSON or
## XML representation.

## API doc: http://dev.opentripplanner.org/apidoc

import requests
import json
from conf import ec2ip

routers = ["denver", "houston", "austin", "tucson", "eipaso"]

# all should return valid routing plan of public transit
router2pos = {
    'denver': {'from': '39.75907,-104.99724', 'to': '39.72650,-104.99145'},
    'austin': {'from': '30.2859758,-97.7404588', 'to': '30.2727757,-97.7522587'},
    'houston': {'from': '29.7180255,-95.4002109', 'to': '29.7199535,-95.3444274'},
    'eipaso': {'from': '31.76000, -106.49157', 'to': '31.75236, -106.47984'},
    # UofA -> Metropia office
    # 'tucson': {'from': '32.23114, -110.94548', 'to': '32.2866043,-110.9473657'},
    # UofA -> Downtown
    'tucson': {'from': '32.2315175,-110.9565735', 'to': '32.22188, -110.96612'},
}


# Make a routing request of OTP server
def route(router):
    url = "{}/otp/routers/{}/plan".format(ec2ip, router)
    payload = {
        'fromPlace': '{}'.format(router2pos[router]['from']),
        'toPlace': '{}'.format(router2pos[router]['to']),
        'time': '8:30am',
        'date': '1-3-2018',
        'mode': 'TRANSIT,WALK',
        # 'mode': 'BICYCLE',
        'maxWalkDistance': '804.672',
        'arriveBy': 'false',
        'wheelchair': 'false',
        'locale': 'en',
    }

    ret = requests.get(url, params=payload)
    # print(ret.url)
    if ret.ok:
        # print (ret.status_code)
        print (ret.text)
    else:
        print (ret.status_code)


if __name__ == '__main__':
    from sys import argv
    if (len(argv) < 2):
        print('Usage: {} <name of router>'.format(argv[0]))
        exit(-1)

    route(argv[1])