from pydantic import BaseModel, Field
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
    amount: float = Field(ge=0)
    quantity: Optional[str] = Field(
        default=None, 
        pattern=r'^[a-zA-Z0-9\s\-\/]*$', 
        description="Optional alphanumeric quantity e.g. '1 Lot' or '3 Workers / 2 Days'"
    )

class ProjectInfo(BaseModel):
    title: str

class DocumentPayload(BaseModel):
    document_id: str
    date_issued: date
    sender: CompanyInfo
    recipient: CompanyInfo
    project: ProjectInfo
    
    # Categorized line items (Stacked sections)
    main_materials: List[LineItem] = []
    labor_and_other: List[LineItem] = []
    
    # Category Totals & Grand Total
    main_materials_total: float = Field(default=0.0, ge=0)
    labor_other_total: float = Field(default=0.0, ge=0)
    total: float = Field(ge=0)
    
    notes: Optional[str] = None