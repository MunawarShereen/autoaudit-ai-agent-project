from pydantic import BaseModel, HttpUrl

class AuditRequest(BaseModel):
    repo_url: HttpUrl  