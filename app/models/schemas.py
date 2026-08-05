from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class CompanyInfo(BaseModel):
    name: str
    address: str
    logo_url: Optional[str] = None
    email: str
    contact: str

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float

class ProjectInfo(BaseModel):
    title: str


class DocumentPayload(BaseModel):
    document_id: str
    date_issued: date
    sender: CompanyInfo
    recipient: CompanyInfo
    project: ProjectInfo
    items: List[LineItem]
    subtotal: float
    tax: float
    total: float
    notes: Optional[str] = None
    

class UserCreate(BaseModel):
    name: str
    age: int
