from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId

class QueryAnswer(BaseModel):
    query: str = Field(..., description="Query text created by user")
    answers: List[str] = Field(..., description="Multiple answers for the query")


class QueriesGot(BaseModel):
    userId: Optional[ObjectId] = Field(None, description="Original user who asked the query")
    queryId: Optional[str] = Field(None, description="Optional query reference ID")
    queryText: str = Field(..., description="Query text assigned to moderator")
    answered: bool = Field(default=False)
    response: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str  # "learner" or "moderator"


class UserCreate(UserBase):
    password: str
    skills: List[str]
    queries: List[QueryAnswer] = []
    queriesGot: List[QueriesGot] = []


class UserResponse(UserBase):
    id: str
    skills: List[str]
    queries: List[QueryAnswer]
    queriesGot: List[QueriesGot]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
