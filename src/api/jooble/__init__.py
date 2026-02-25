"""
job_title='Java Full Stack Developer - Hybrid / Partially Client Onsite' job_location='Irving, TX' job_snippet="&nbsp;...data processing, and handling the functionality that users don't see. This involves using server-side languages and frameworks (e.g., <b>Python,</b> Java, Node.js, PHP, Ruby). \r\n Building and integrating robust, secure, and efficient APIs (Application Programming Interfaces),...&nbsp;" job_salary='' job_source='successfactors.com' job_type='' job_link='https://jooble.org/desc/-7948357601433977685' job_company='NTT DATA Services' job_updated='2026-02-22T11:04:54.3070000' job_id=-7948357601433977685
"""

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
    return [Job(**job) for job in parsed.get("jobs", [])]
