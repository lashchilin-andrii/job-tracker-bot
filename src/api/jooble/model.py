from pydantic import BaseModel


class JoobleJob(BaseModel):
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
