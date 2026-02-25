from pydantic import BaseModel, Field, ConfigDict


class JoobleJob(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    job_title: str = Field(validation_alias="title")
    job_location: str = Field(validation_alias="location")
    job_snippet: str = Field(validation_alias="snippet")
    job_salary: str | None = Field(default=None, validation_alias="salary")
    job_source: str = Field(validation_alias="source")
    job_type: str | None = Field(default=None, validation_alias="type")
    job_link: str = Field(validation_alias="link")
    job_company: str | None = Field(default=None, validation_alias="company")
    job_updated: str = Field(validation_alias="updated")
    job_id: int = Field(validation_alias="id")
