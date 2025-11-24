from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    SECRET_KEY: str = "chave_padrao_seguranca" # Valor padrão
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Define um valor padrão caso não esteja no .env
    MONGODB_URL: str = "mongodb://mongo:27017/argos_db" 

    class Config:
        env_file = ".env"

settings = Settings()