from pydantic import BaseModel
from typing import Literal


class ServiceCreate(BaseModel):
    name: str
    url: str
    owner: str = "MIS Team"


class ServiceStatusUpdate(BaseModel):
    status:Literal["unknown", "online", "offline","degraded"]
