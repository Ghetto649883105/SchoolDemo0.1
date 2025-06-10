from pydantic import BaseModel


class UserIn(BaseModel):
    user_id: str
    password: str
