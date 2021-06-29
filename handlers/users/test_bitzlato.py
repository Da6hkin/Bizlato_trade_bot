import datetime
import http
import python_http_client
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

# secret user key
key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "dWTemrvbTSZkCWap5lWVPjdKrdUBxrNGJlvY52L97A8",
       "y": "TUy3E7CrPFQMy0ZI_ffpGJGwuWsdeChvRJEqs1c4TBA", "d": "Aji6FzaGjlqxSqAWIRzPKLFxQhZXekPkGbrQRgRiHyY"}

dt = datetime.datetime.now()
ts = time.mktime(dt.timetuple())
claims = {
    # user identificator
    "email": "annabychkova123@rambler.ru",
    # leave as is
    "aud": "usr",
    # token issue time
    "iat": int(ts),
    # unique token identificator
    "jti": hex(random.getrandbits(64))
}
print(claims)


token = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJlbWFpbCI6ImFubmFieWNoa292YTEyM0ByYW1ibGVyLnJ1IiwiYXVkIjoidXNyIiwiaWF0IjoxNjI0ODc1Mjc5LCJqdGkiOiIweDY3MzBiMDBkNDRjZGIyNjYifQ.rzEeBOprFgwwI5iHanZLloJUpllrj_mOLRk7mRj7-oklvKy4Sgtr87HgmwBVtpmbT8yNTILRCowNdvDXJ4Kvww"
print(type(token))
resp = requests.get('https://bitzlato.com/api/p2p/trade/', headers={
    "Authorization": "Bearer " + token
},
                    params={})
print(resp.status_code, resp.reason, resp.text)
