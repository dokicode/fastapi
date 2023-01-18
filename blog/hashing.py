from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():

    

    def get_password_hash(password):
        
        return pwd_context.hash(password)

    def verify(password, hashed_password):
        try:
            return pwd_context.verify(password, hashed_password)
        except Exception as e:
            print(e)
            return None