import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from models import schemas
import bcrypt
import jwt

load_dotenv()

# Função para cadastrar um usuário no banco de dados. Realiza uma verificação para garantir
# que não exista um nome de usuário duplicado no sistema, retornando um erro se já existir.
# A senha fornecida pelo usuário é transformada em bytes, e em seguida um salt é gerado para
# realizar o hash da senha usando bcrypt, adicionando uma camada extra de segurança em caso
# de vazamento de dados. Após o hash, a senha é armazenada no banco de dados juntamente com o salt.
# Um token JWT é gerado com o nome de usuário e o ID do usuário, e retornado para o cliente
# como parte da resposta, permitindo o uso do token para autenticação em chamadas futuras.
def create_user(db: Session, user: schemas.User):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já existe")

    bytes_password = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    password = hashed_password.decode('utf-8')
    db_user = User(name=user.name, password=password, salt=salt)
    db.add(db_user)
    db.commit()
    token = jwt.encode({"username": user.name, "user_id": db_user.id}, os.getenv("JWT_SECRET"))
    return {"message": "Usuário criado com sucesso", "auth_token": token}

# Função para autenticar um usuário. Realiza uma consulta no banco de dados
# buscando o nome de usuário. Se o usuário for encontrado, compara a senha fornecida
# com a senha armazenada (que foi hashada com bcrypt). Se a senha estiver correta,
# retorna um token de autenticação. Caso o usuário ou senha estejam incorretos,
# levanta uma exceção HTTP correspondente.
def authenticate(db: Session, user: schemas.User):
    db_user = db.query(User).filter(User.name == user.name).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), db_user.salt)
    str_hashed_password = hashed_password.decode('utf-8')

    db_user = db.query(User).filter(User.name == user.name, User.password == str_hashed_password).first()

    if db_user:
        token = jwt.encode({"username": db_user.name, "user_id": db_user.id}, os.getenv("JWT_SECRET"))
        return {"message": "Usuário autenticado com sucesso", "auth_token": token}

    raise HTTPException(status_code=404, detail="Senha incorreta")
