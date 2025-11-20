from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema base para um token de acesso.
    Usado em rotas que retornam apenas o access_token (ex: refresh).
    """
    access_token: str
    token_type: str
    tipo: str

class TokenResponseSchema(Token):
    """
    Schema completo para a resposta do endpoint de login.
    Inclui o access_token e o refresh_token.
    """
    refresh_token: str

class TokenData(BaseModel):
    """
    Schema para os dados contidos dentro do payload do JWT.
    """
    id: int | None = None
    tipo: str | None = None