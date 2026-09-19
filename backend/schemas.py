from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TripRequest(BaseModel):
    destination: str
    days: int
    interests: str

class DayPlan(BaseModel):
    day:int
    title: str
    activities: list[str]
    food: list[str]
    tips: list[str]

class GeneratePlan(BaseModel):
    summary: str
    days: list[DayPlan]    


class TripResponse(BaseModel):
    id: int
    destination: str
    days: int
    interests: str
    generated_plan: GeneratePlan
    user_id: int

    model_config = ConfigDict(from_attributes=True)