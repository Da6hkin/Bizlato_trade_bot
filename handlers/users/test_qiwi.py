import requests

api_access_token = "d34f19e80e75768632cc999fce24dc21"


def get_profile(api_access_token):
    s7 = requests.Session()
    s7.headers['Accept'] = 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    p = s7.get(
        'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    if p.status_code == 200:
        return p.json()["contractInfo"]["contractId"]
    else:
        return 0


print(get_profile(api_access_token))
