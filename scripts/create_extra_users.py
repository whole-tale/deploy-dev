import requests
from requests.auth import HTTPBasicAuth

users = [
    {
        "firstName": "Alicja",
        "lastName": "Smith",
        "login": "ala123",
        "email": "ala@localhost.com",
        "admin": False,
        "password": "password",
    },
    {
        "firstName": "Barbara",
        "lastName": "Smith",
        "login": "basia",
        "email": "basia@localhost.com",
        "admin": False,
        "password": "password",
    },
]

headers = {"Content-Type": "application/json", "Accept": "application/json"}
api_url = "https://girder.local.wholetale.org/api/v1"

for user in users:
    try:
        r = requests.post(api_url + "/user", params=user, headers=headers)
        r.raise_for_status()
    except requests.HTTPError:
        if r.status_code == 400:
            r = requests.get(
                api_url + "/user/authentication",
                auth=HTTPBasicAuth(user["login"], user["password"]),
            )
            r.raise_for_status()
        else:
            raise
    except Exception:
        print("Girder is no longer running")
        raise

    token = r.json()["authToken"]["token"]
    print(f"https://dashboard.local.wholetale.org/login?token={token} # {user['login']}")
