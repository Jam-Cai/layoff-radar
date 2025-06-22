from pydantic import BaseModel
from typing import Optional

class Features(BaseModel):
    Location_HQ: str
    Industry: str
    Stage: str
    Year: int
    log10_Funds_Raised: int
