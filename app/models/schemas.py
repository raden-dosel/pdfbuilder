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
    main_materials_cost: float = Field(default=0.0, ge=0)
    labor_other_cost: float = Field(default=0.0, ge=0)
    # Optional alphanumeric quantity for labor/other materials
    labor_other_qty: Optional[str] = Field(
        default=None, 
        pattern=r'^[a-zA-Z0-9\s\-\/]*$', 
        description="Optional alphanumeric quantity e.g. '2 Workers / 3 Days'"
    )

class ProjectInfo(BaseModel):
    title: str

class DocumentPayload(BaseModel):
    document_id: str
    date_issued: date
    sender: CompanyInfo
    recipient: CompanyInfo
    project: ProjectInfo
    items: List[LineItem]
    
    # Category Totals & Grand Total
    main_materials_total: float = Field(default=0.0, ge=0)
    labor_other_total: float = Field(default=0.0, ge=0)
    total: float = Field(ge=0)
    
    notes: Optional[str] = None