from pydantic import BaseModel, Field, ConfigDict, field_validator
import html
import re


class Job(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    job_title: str = Field(validation_alias="title")
    job_location: str = Field(validation_alias="location")
    job_snippet: str | None = Field(default=None, validation_alias="snippet")
    job_salary: str | None = Field(default=None, validation_alias="salary")
    job_source: str = Field(validation_alias="source")
    job_type: str | None = Field(default=None, validation_alias="type")
    job_link: str | None = Field(default=None, validation_alias="link")
    job_company: str | None = Field(default=None, validation_alias="company")
    job_updated: str | None = Field(default=None, validation_alias="updated")
    job_id: int = Field(validation_alias="id")

    @field_validator("job_snippet", mode="before")
    @classmethod
    def clean_snippet(cls, v):
        if not v:
            return v

        v = html.unescape(v)
        v = v.replace("\xa0", " ").replace("\u200b", "")
        v = v.replace("...", " ")
        v = re.sub(r"<.*?>", "", v)
        v = re.sub(r"[ \t]+", " ", v)
        v = re.sub(r"(\r?\n\s*)+", "\n", v)

        return v.strip() + "..."
