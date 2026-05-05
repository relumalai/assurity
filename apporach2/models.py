from typing import List, Optional
from pydantic import BaseModel

class Promotion(BaseModel):
    Id: int
    Name: str
    Description: Optional[str] = None

class Listing(BaseModel):
    Name: str
    Relist: bool
    Promotions: List[Promotion] = []
