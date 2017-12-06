## The OTP Routing API is a RESTful web service that responds
## to journey planning requests with itineraries in a JSON or
## XML representation.

## API doc: http://dev.opentripplanner.org/apidoc

import requests
import json

# Get all stops on Capital Metro (agency id = 1) route 50 (route id)
# 1:50 ---> agency id:route id
url = "http://192.168.56.6:8080/otp/routers/default/index/routes/1:50/stops"
payload = {'detail': 'false', 'refs': 'true'}
ret = requests.get(url, params=payload)
if ret.ok:
    print (ret.status_code)
    print (ret.json())
else:
    print (ret.status_code)


# Get all routes passing through Capital Metro (agency id = 1) stop 252
url = "http://192.168.56.6:8080/otp/routers/default/index/stops/1:252/routes"
ret = requests.get(url)
if ret.ok:
    # print (ret.json())
    print (ret.status_code)
else:
    print (ret.status_code)


# Get all stop patterns used by trips on the given route
# All unique sequences of stops on the Capital Metro route 1 (route id)
url = "http://192.168.56.6:8080/otp/routers/default/index/routes/1:1/patterns"
ret = requests.get(url)
if ret.ok:
    print (ret.json())
else:
    print (ret.status_code)
