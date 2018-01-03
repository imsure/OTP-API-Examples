## The OTP Routing API is a RESTful web service that responds
## to journey planning requests with itineraries in a JSON or
## XML representation.

## API doc: http://dev.opentripplanner.org/apidoc

import requests
import json

ec2ip = "http://34.212.174.108:8080"
routers = ["pdx", "houston", "austin", "tucson"]

# Get A list of all routers
# url = "http://192.168.56.6:8080/otp/routers/default"
# ret = requests.get(url)
# print (ret.status_code)
# print (ret.json())


# Get a list of all GTFS routes on the default router (currently austin only)
# url = "http://192.168.56.6:8080/otp/routers/default/index/routes"
# ret = requests.get(url)
# print (ret.status_code)
# print (ret.json())


# Trip planning example
url = "http://34.212.174.108:8080/otp/routers/austin/plan"
payload = {'fromPlace': '30.283529283816247,-97.7340316772461',
           'toPlace': '30.220805190457803,-97.79720306396484',
           'time': '4:29pm',
           'date': '12-11-2017',
           'mode': 'TRANSIT,WALK',
           'maxWalkDistance': '804.672',
           'arriveBy': 'false',
           'wheelchair': 'false',
           'locale': 'en'}
           # 'itinIndex': '1'}
# ret = requests.get(url, params=json.dumps(payload)) // no JSON! just pass dict directly
ret = requests.get(url, params=payload)
print (ret.url)
if ret.ok:
    print (ret.status_code)
    # print (ret.json())
else:
    print (ret.status_code)


# Get all routes passing through TriMet (agency id) stop 7003 in Portland
url = "http://34.212.174.108:8080/otp/routers/pdx/index/stops/TriMet:7003/routes"
ret = requests.get(url)
if ret.ok:
    print (ret.json())
    print (ret.status_code)
else:
    print (ret.status_code)
