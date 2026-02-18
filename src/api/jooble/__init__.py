from src.config import ApiConfig
import http.client
import json
from src.api.jooble.model import JoobleJob


def search_jobs(keywords: str, location: str) -> list[JoobleJob]:
    body = json.dumps({"keywords": keywords, "location": location})
    connection = http.client.HTTPSConnection("jooble.org")
    headers = {"Content-type": "application/json"}
    connection.request("POST", f"/api/{ApiConfig().JOOBLE_API_KEY}", body, headers)
    response = connection.getresponse()
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    return [JoobleJob(**job) for job in parsed.get("jobs", [])]


jobs = search_jobs("python", "Remote")
for job in jobs:
    print(job)
    print()
    print()
