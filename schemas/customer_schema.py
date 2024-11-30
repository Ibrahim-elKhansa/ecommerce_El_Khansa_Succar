from pydantic import BaseModel

class CustomerBase(BaseModel):
    username: str
    wallet_balance: float

    class Config:
        orm_mode = True
        from_attributes = True


class CustomerCreate(CustomerBase):
    password: str
    full_name: str
    age: int
    address: str
    gender: str
    marital_status: str


class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
