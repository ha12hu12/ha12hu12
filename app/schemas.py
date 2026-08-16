from pydantic import BaseModel, EmailStr
from datetime import datetime
#posts schemas
class post_get_schema(BaseModel):
    title: str
    content: str
    created_at: datetime
    owner_id: int

class post_create_out_schema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int

class post_create_data_schema(BaseModel):
    title: str
    content: str

class post_update_data_schema(BaseModel):
    title: str
    content: str
#user schemas
class user_create_out_schema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class user_create_data_schema(BaseModel):
    email:  EmailStr
    password: str

class user_get_out_schema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
 #user authentication
class user_login_schema(BaseModel):
    email:EmailStr
    password: str

class data_to_encode_schema(BaseModel):
    id: dict

class token_info(BaseModel):
    id:int

#vote schemas
class vote_data_schema(BaseModel):
    post_id: int
    dir: bool