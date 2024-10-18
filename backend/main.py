from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from auth import verify_jwt
from controllers import list_items_controller, users_controller
from db.database import get_db
from models import schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adiciona o middleware CORSMiddleware à aplicação FastAPI, permitindo requisições entre
# origens diferentes (Cross-Origin Resource Sharing).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todo-list-bucket.nyc3.digitaloceanspaces.com", "http://localhost:5500"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Declara todas as rotas com seus respectivos métodos HTTP e middlewares, representado pela função
# `Depends` dentro dos parâmetros da função.

@app.post("/sign-up")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    return users_controller.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.User, db: Session = Depends(get_db)):
    return users_controller.authenticate(db=db, user=user)

@app.post("/todo-list", response_model=schemas.ListItem)
def create_list_item(item: schemas.ListItemCreate,
                     db: Session = Depends(get_db), 
                     payload: dict = Depends(verify_jwt),
                     ):
    return list_items_controller.create_list_item(db=db, item=item, payload=payload)

@app.get("/todo-list")
def get_list_items(db: Session = Depends(get_db), 
                   payload: dict = Depends(verify_jwt)):
    return list_items_controller.get_list_items(db=db, payload=payload)

@app.put("/todo-list/status/{item_id}")
def update_item_status(item_id: str,
                       db: Session = Depends(get_db), 
                       payload: dict = Depends(verify_jwt)):
    return list_items_controller.update_item_status(db=db, item_id=item_id, payload=payload)


@app.delete("/todo-list/{item_id}")
def delete_item(item_id: str,
                db: Session = Depends(get_db), 
                payload: dict = Depends(verify_jwt)):
    return list_items_controller.delete_item(db=db, item_id=item_id, payload=payload)
