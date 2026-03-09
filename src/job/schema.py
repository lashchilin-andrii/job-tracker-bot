from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
import html
import re


class Job(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    job_id: str = Field(validation_alias="id")
    job_title: str = Field(validation_alias="title")
    job_location: str = Field(validation_alias="location")
    job_snippet: str | None = Field(default=None, validation_alias="snippet")
    job_salary: str | None = Field(default=None, validation_alias="salary")
    job_source: str = Field(validation_alias="source")
    job_type: str | None = Field(default=None, validation_alias="type")
    job_link: str | None = Field(default=None, validation_alias="link")
    job_company: str | None = Field(default=None, validation_alias="company")
    job_updated: str | None = Field(default=None, validation_alias="updated")

    @field_validator("job_id", mode="before")
    @classmethod
    def convert_job_id_to_str(cls, v: str):
        return str(v)

    @field_validator("job_location", mode="after")
    @classmethod
    def add_flag(cls, v: str):
        if not v:
            return v

        if "Remote" in v:
            return f"{v} 🌍"

        return v

    @field_validator("job_snippet", mode="before")
    @classmethod
    def clean_snippet(cls, v):
        if not v:
            return v

        v = html.unescape(v)

        v = re.sub(r"<.*?>", "", v)
        v = re.sub(r"&##(\d+);", r"&#\1;", v)
        v = v.replace("\xa0", " ").replace("\u200b", "")
        v = v.replace("**", " ")
        v = re.sub(r"\s+", " ", v)

        v = v.strip()

        if not v:
            return None

        return v[:300]

    @field_validator("job_updated", mode="before")
    @classmethod
    def format_updated(cls, v: str):
        if not v:
            return v

        v = re.sub(r"\.(\d{6})\d*", r".\1", v)

        try:
            dt = datetime.fromisoformat(v)
            return dt.strftime("%d %b %Y")
        except ValueError:
            return v
