from src.exceptions import Absent
from src.config import ApiConfig
import http.client
import json
from src.job.schema import Job


def get_jobs(keywords: str, location: str) -> list[Job]:
    body = json.dumps({"keywords": keywords, "location": location})
    connection = http.client.HTTPSConnection("jooble.org")
    headers = {"Content-type": "application/json"}
    connection.request("POST", f"/api/{ApiConfig().JOOBLE_API_KEY}", body, headers)
    response = connection.getresponse()
    data = response.read().decode("utf-8")
    parsed = json.loads(data)

    jobs_data = parsed.get("jobs", [])
    if not jobs_data:
        raise Absent("No jobs found for the given keywords and location.")

    return [Job(**job) for job in jobs_data]
