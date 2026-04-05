from pydantic import BaseModel, HttpUrl

class AuditRequest(BaseModel):
    repo_url: HttpUrl  # Ye automatically validate karega ke URL format theek hai