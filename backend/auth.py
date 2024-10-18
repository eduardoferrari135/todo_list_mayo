import os
import jwt
from fastapi import HTTPException, Request
from dotenv import load_dotenv

load_dotenv()

# Função para verificar o token JWT presente no header da requisição.
# O header deve conter o token no formato "Bearer {token}".
# Se o header de autorização estiver ausente ou não seguir o formato correto, uma exceção HTTP é levantada.
# Após extrair o token, a função tenta decodificá-lo usando a chave secreta definida nas variáveis de ambiente.
# Em caso de erro, são levantadas exceções específicas, como token expirado ou inválido.
def verify_jwt(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Not authenticated")
    
    # Extraí token do header da requisição
    token = auth_header.split(" ")[1]
    
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")
