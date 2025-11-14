from beanie import Document
from pydantic import EmailStr,Field
import bcrypt
class User(Document):
    username : str = Field (...,min_length=3,max_length = 50)
    email : EmailStr
    password_hash : str

    class Settings:
        collection = "users"

    @staticmethod
    def hash_password(password:str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'),salt).decode('utf-8')
    
    @staticmethod
    def verfiy_password(password:str,password_hash:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'),password_hash.encode('utf-8'))



