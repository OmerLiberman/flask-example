import requests

URL = "http://127.0.0.1:5000/"

print("PUT requests:")
for i in range(1, 10):
	resp = requests.put(URL + f"video/{i}", {'name': f"Ironman{i}",
									  "views": 100 + i, 'likes': 10 + i})
	print(resp.status_code, resp.json())

print("GET requests:")
resp = requests.get(URL + "video/50")
print(resp.status_code, resp.json())


print("UPDATE request:")
resp = requests.patch(URL + "video/1", {"name": "Ironman1", "views": 15})
print(resp.status_code, resp.json())

print("DELETE request:")
resp = requests.delete(URL + "video/1")
print(resp.status_code)
