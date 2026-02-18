import http.client

host = "jooble.org"
key = "09dc1ce1-762b-4969-9d9c-a8075ef64352"

connection = http.client.HTTPConnection(host)
# request headers
headers = {"Content-type": "application/json"}
# json query
body = "{'keywords': 'python', 'location': 'Remote'}"
connection.request("POST", "/api/" + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
print(response.read())
