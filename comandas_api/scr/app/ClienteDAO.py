from fastapi import APIRouter, Depends
from domain.entities.Cliente import Cliente
import db
from infra.orm.ClienteModel import ClienteDB
from typing import Annotated
from security import get_current_active_user, User

router = APIRouter(dependencies=[Depends(get_current_active_user)])

# Rota para buscar todos os clientes
@router.get("/cliente/", tags=["Cliente"])
async def get_cliente(current_user: Annotated[User, Depends(get_current_active_user)]):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).all()
        return {"dados": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para buscar um cliente específico pelo ID
@router.get("/cliente/{id}", tags=["Cliente"])
async def get_cliente_por_id(id: int):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).all()
        return {"dados": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para adicionar um novo cliente
@router.post("/cliente/", tags=["Cliente"])
async def post_cliente(corpo: Cliente):
    try:
        session = db.Session()
        dados = ClienteDB(
        nome=corpo.nome,
        cpf=corpo.cpf,
        telefone=corpo.telefone
)
        session.add(dados)
        session.commit()
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para atualizar um cliente existente
@router.put("/cliente/{id}", tags=["Cliente"])
async def put_cliente(id: int, corpo: Cliente):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        session.add(dados)
        session.commit()
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para excluir um cliente pelo ID
@router.delete("/cliente/{id}", tags=["Cliente"])
async def delete_cliente(id: int):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).filter(ClienteDB.id_cliente == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_cliente}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Verifica se um CPF já está cadastrado e retorna os dados se estiver
@router.get("/cliente/cpf/{cpf}", tags=["Cliente - Valida CPF"])
async def cpf_cliente(cpf: str):
    try:
        session = db.Session()
        dados = session.query(ClienteDB).filter(ClienteDB.cpf == cpf).all()
        return {"dados": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()
