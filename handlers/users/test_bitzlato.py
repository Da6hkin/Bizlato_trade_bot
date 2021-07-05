import datetime
import http
import python_http_client
import time
import random

import requests
from jose import jws
from jose.constants import ALGORITHMS

# secret user key
key = {"kty": "EC", "alg": "ES256", "crv": "P-256", "x": "BNyT8k9yJl0JZhjwTpEes18pBjivw1vPjt9lWOUkHnQ",
       "y": "Yz5hWfLA3Wz6d2pwydc3sqQLCluIc1irf7SoJQJG3Q4", "d": "7tBk9TEjHHqU87MELA5p5MC2BjtlqMIDwcg__WszKag"}

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
token = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJlbWFpbCI6ImFsaW53YXIuY3Jld0Bwcm90b25tYWlsLmNvbSIsImF1ZCI6InVzciIsImlhdCI6MTYyNTA1OTMxNywianRpIjoiMHhlNTk5OTYxNjRkMmNkZTQzIn0.jv-yZpeYl4yNuPaUS9J4cNV5Y0Rbv5RbHgqjUTjsMDnheKqdx90HRl2YJVC8kj-RkZAhvAJd_K4PAIQAf-7XaQ"

resp = requests.get('https://bitzlato.com/api/p2p/trade/', headers={
    "Authorization": "Bearer " + token
},
                    params={})
print(resp.status_code, resp.reason, resp.text)
