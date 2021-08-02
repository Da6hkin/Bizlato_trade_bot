import datetime
import http
import python_http_client
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

# secret user key
# key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "dWTemrvbTSZkCWap5lWVPjdKrdUBxrNGJlvY52L97A8",
#        "y": "TUy3E7CrPFQMy0ZI_ffpGJGwuWsdeChvRJEqs1c4TBA", "d": "Aji6FzaGjlqxSqAWIRzPKLFxQhZXekPkGbrQRgRiHyY"}
key = {'kty': 'EC', 'alg': 'ES256', 'crv': 'P-256', 'x': '7Cq3do5cVWuGBIMLUeUViuljwraWyh2LZLOzrh0TxWQ', 'y': 'mbUuyEMGfG0V9wlUqAWvEN_vXmFXwQRkm_XvL5ZPvzQ', 'd': 'vYma0PPHc-6lEf9zmtXHbdWLiM1wMMV1rdBw8p-qb0I'}

dt = datetime.datetime.now()
ts = time.mktime(dt.timetuple())
claims = {
    # user identificator
    "email": "alinwar.crew@protonmail.com",
    # leave as is
    "aud": "usr",
    # token issue time
    "iat": int(ts),
    # unique token identificator
    "jti": hex(random.getrandbits(64))
}
print(claims)
token = jws.sign(claims, key, headers={"kid": "2"}, algorithm=ALGORITHMS.ES256)

resp = requests.get('https://bitzlato.com/api/p2p/trade/', headers={
    "Authorization": "Bearer " + token
},
                    params={})
print(resp.status_code, resp.reason, resp.text)
