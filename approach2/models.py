from typing import List, Optional
from pydantic import BaseModel

#Patially assumed and generated models.


class Promotion(BaseModel):
    Id: int
    Name: str
    Description: Optional[str] = None


class Listing(BaseModel):
    Name: str
    CanRelist: bool
    Promotions: List[Promotion] = []
