from pydantic import BaseModel


class Job(BaseModel):
    title: str
    location: str
    snippet: str
    salary: str
    source: str
    type: str
    link: str
    company: str
    updated: str
    id: int
