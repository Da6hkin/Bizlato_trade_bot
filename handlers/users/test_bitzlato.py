import datetime
import http
import python_http_client
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

# secret user key
key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "BZZNXLMnglY0RCVgcmmkQWivv30-c81Q6zvTUDps8UQ",
       "y": "bZZU507c_I7D2g-vgRXwcvYLR1T2nzNR4g2W16ue_1A", "d": "owNbkrQ3AwQZIboQSd3_lzsIkrxf-bKMnxVHsEigJho"}

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

token = jws.sign(claims, key, headers={"kid": "1"}, algorithm=ALGORITHMS.ES256)
print(token)
print(type(token))
resp = requests.get('https://bitzlato.com/api/p2p/trade/', headers={
            "Authorization": "Bearer " + token
        },
            params={})
print(type(resp.status_code), resp.reason, resp.text)
