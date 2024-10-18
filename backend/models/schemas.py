from typing import Optional
from pydantic import BaseModel

# Classes utilizadas para a validação e formatação do body das requisições

class User(BaseModel):
    name: str
    password: str

class ListItem(BaseModel):
    task: str
    id: str
    user_id: str
    status: str

class ListItemCreate(BaseModel):
    task: str

class ListItemUpdate(BaseModel):
    task: str
    id: str

class TokenData(BaseModel):
    username: Optional[str] = None
