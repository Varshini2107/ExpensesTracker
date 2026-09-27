import urllib.request
import json

data = {
    "name": "Test Lunch",
    "category": "Food",
    "amount": 200,
    "date": "2026-09-27"
}

data = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    "http://127.0.0.1:5000/expenses",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

response = urllib.request.urlopen(request)

print(response.read().decode())