import http.client
import json

from src.config import ApiConfig

host = "jooble.org"

connection = http.client.HTTPConnection(host)

headers = {"Content-type": "application/json"}

body = json.dumps({"keywords": "python", "location": "Remote"})

connection.request("POST", "/api/" + ApiConfig().JOOBLE_API_KEY, body, headers)
response = connection.getresponse()

data = response.read().decode("utf-8")
parsed = json.loads(data)

# Pretty print JSON
print(json.dumps(parsed, indent=4, ensure_ascii=False))
