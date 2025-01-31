from pydantic import BaseModel, Field

class KRATaxSchema(BaseModel):
    """Validation schema for KRA taxpayer records"""
    pin: str = Field(..., regex=r'^[A-Z]\d{9}[A-Z]$')
    declared_income: float = Field(..., gt=0)
    sector: str = Field(..., max_length=4)
    last_filing: datetime