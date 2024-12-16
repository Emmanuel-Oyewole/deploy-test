from pydantic import BaseModel

class Token(BaseModel):
    id: str
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str