## The OTP Routing API is a RESTful web service that responds
## to journey planning requests with itineraries in a JSON or
## XML representation.

## API doc: http://dev.opentripplanner.org/apidoc

import requests
import json

# Get A list of all routers
url = "http://192.168.56.6:8080/otp/routers/default"
ret = requests.get(url)
print (ret.status_code)
print (ret.json())

# Get a list of all GTFS routes on the default router (???)
url = "http://192.168.56.6:8080/otp/routers/default/index/routes"
ret = requests.get(url)
print (ret.status_code)
# print (ret.json())

# Trip planning example
url = "http://192.168.56.6:8080/otp/routers/default/plan"
head= {"Accept": "applicaiton/json",
       "Content-type": "application/json"}
payload = {'fromPlace': '30.283529283816247,-97.7340316772461',
           'toPlace': '30.220805190457803,-97.79720306396484',
           'time': '10:29pm',
           'date': '12-05-2017',
           'mode': 'TRANSIT,WALK',
           'maxWalkDistance': '804.672',
           'arriveBy': 'false',
           'wheelchair': 'false',
           'locale': 'en',
           'itinIndex': '0'}
# ret = requests.get(url, params=json.dumps(payload))
ret = requests.get(url, params=payload)
print (ret.url)
if (ret.ok):
    print (ret.json())
else:
    print (ret.status_code)
