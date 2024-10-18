import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import schemas
from models.list_item import ListItem
from db.redis_client import r

# Função para obter os itens de uma lista de tarefas. Realiza uma verificação no cache Redis
# usando o `user_id` como chave. Se os dados estiverem no cache, são retornados diretamente.
# Caso contrário, realiza uma consulta ao banco de dados para obter a lista de tarefas do usuário
# e armazena o resultado em cache para otimizar chamadas futuras. Retorna a lista de tarefas pertencentes
# ao usuário.
def get_list_items(db: Session, payload: dict):
    cache_key = f"todo-list-{payload.get("user_id")}"

    cache = r.get(cache_key)
    if cache:
        return json.loads(cache)

    todo_list = db.query(ListItem).filter(ListItem.user_id == payload.get("user_id")).all()
    todo_list_dict = [item.to_dict() for item in todo_list]
    r.set(cache_key, json.dumps(todo_list_dict))

    return todo_list

# Função para criar um novo item de lista de tarefas. O item criado é associado ao `user_id`
# presente no payload, e após ser salvo no banco de dados, o cache correspondente à lista de
# tarefas do usuário é invalidado (deletado) para garantir que consultas futuras retornem a lista
# mais atualizada. Retorna o item criado.
def create_list_item(db: Session, item: schemas.ListItemCreate, payload: dict):
    db_item = ListItem(user_id=payload.get("user_id"), task=item.task, status="Pendente")
    db.add(db_item)
    db.commit()
    r.delete(f"todo-list-{payload.get("user_id")}")
    return db_item

# Função para deletar um item de lista de tarefas. Realiza uma consulta ao banco de dados com base
# no `item_id` e `user_id`. Se o item não for encontrado, uma exceção é levantada. Caso o item exista,
# ele é deletado do banco de dados e o cache relacionado à lista de tarefas do usuário é invalidado.
# Retorna uma mensagem de sucesso.
def delete_item(db: Session, item_id: str, payload: dict):
    item = db.query(ListItem).filter(ListItem.id == item_id, ListItem.user_id == payload.get("user_id")).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    db.delete(item)
    db.commit()
    r.delete(f"todo-list-{payload.get("user_id")}")
    return {"message": "Item deletado com sucesso"}

# Função para atualizar o status de um item de lista de tarefas. Consulta o banco de dados usando
# o `item_id` e `user_id` do payload da requisição. Se o item não for encontrado, uma exceção é levantada.
# Se encontrado, o status do item é alternado entre "Pendente" e "Completa", o banco de dados é atualizado
# e o cache relacionado à lista de tarefas do usuário é invalidado.
def update_item_status(db: Session, item_id: str, payload: dict):

    item = db.query(ListItem).filter(ListItem.id == item_id, ListItem.user_id == payload.get("user_id")).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    if item.status == "Pendente":
        item.status = "Completa"
    else:
        item.status = "Pendente"

    db.commit()
    db.refresh(item)

    r.delete(f"todo-list-{payload.get("user_id")}")
    return {"message": "Status atualizado com sucesso"}
