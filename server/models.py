from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# layover schemas
class LayoverBase(BaseModel):
    layoff_count: Optional[int] = None
    funding_raised: Optional[int] = None
    type_of_company: Optional[str] = None
    country: Optional[str] = None
    industry: Optional[str] = None
    company_name: Optional[str] = None
    risk_level: Optional[float] = None
    additional_info: Optional[str] = None
    explaination: Optional[str] = None

class addLayover(LayoverBase):
    pass

class Layover(LayoverBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True