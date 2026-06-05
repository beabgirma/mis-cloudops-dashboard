from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    url: str
    owner: str = "MIS Team"


class ServiceStatusUpdate(BaseModel):
    status: str
