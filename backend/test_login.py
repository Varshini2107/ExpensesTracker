import urllib.request
import urllib.error
import json

data = {
    "username": "newuser",
    "password": "12345"
}

data = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    "http://127.0.0.1:5000/login",
    data=data,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    response = urllib.request.urlopen(request)

    print("STATUS:", response.status)
    print("RESPONSE:", response.read().decode())

except urllib.error.HTTPError as error:
    print("STATUS:", error.code)
    print("RESPONSE:", error.read().decode())