import urllib.request
import json

data = {
    "username": "varshini",
    "password": "12345"
}

data = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    "http://127.0.0.1:5000/register",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

response = urllib.request.urlopen(request)

print("STATUS:", response.status)
print("RESPONSE:", response.read().decode())