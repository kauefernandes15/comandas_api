from fastapi import APIRouter
from domain.entities.Funcionario import Funcionario
import db
from infra.orm.FuncionarioModel import FuncionarioDB
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User
router = APIRouter( dependencies=[Depends(get_current_active_user)] )

@router.get("/funcionario/", tags=["Funcionário"], dependencies=[Depends(get_current_active_user)], )
async def get_funcionario( current_user:Annotated[User, Depends(get_current_active_user)], ):
    try:
        session = db.Session()
        # Busca todos
        dados = session.query(FuncionarioDB).all()

        return {"dados": dados}, 200

    except Exception as e:
        # Em caso de erro, retorna a mensagem de erro com status 400 (Bad Request)
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/funcionario/{id}", tags=["Funcionário"])
async def get_funcionario_por_id(id: int):
    try:
        session = db.Session()
# busca um com filtro
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).all()
        return dados, 200
    
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
     session.close()


@router.post("/funcionario/", tags=["Funcionário"])
async def post_funcionario(corpo: Funcionario):
    try:
        session = db.Session()
# cria um novo objeto com os dados da requisição
        dados = FuncionarioDB(
        nome=corpo.nome,
        matricula=corpo.matricula,
        cpf=corpo.cpf,
        telefone=corpo.telefone,
        grupo=corpo.grupo,
        senha=corpo.senha
)
        session.add(dados)
        # session.flush()
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.put("/funcionario/{id}", tags=["Funcionário"])
async def put_funcionario(id: int, corpo: Funcionario):
    try:
        session = db.Session()
# busca os dados atuais pelo id
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
# atualiza os dados com base no corpo da requisição
        dados.nome = corpo.nome
        dados.cpf = corpo.cpf
        dados.telefone = corpo.telefone
        dados.senha = corpo.senha
        dados.matricula = corpo.matricula
        dados.grupo = corpo.grupo
        session.add(dados)
        session.commit()
        return {"id": dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()


@router.delete("/funcionario/{id}", tags=["Funcionário"])
async def delete_funcionario(id: int):
    try:
        session = db.Session()
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.id_funcionario == id).one()
        session.delete(dados)
        session.commit()
        return {"id" : dados.id_funcionario}, 200
    except Exception as e:
        session.rollback()
        return{"erro": str(e)}, 400
    finally:
        session.close()


#verifica se cpf ja ta cadastrado e retorna os dados se estiver
@router.get("/funcionario/cpf/{cpf}", tags=["Funcionario - Valida CPF"])
async def cpf_funcionario(cpf:str):
    try:
        session = db.Session()

        # busca com filtros retornando dados cadastrados
        dados = session.query(FuncionarioDB).filter(FuncionarioDB.cpf == cpf).all()
        return dados, 200
    except Exception as e :
        return {"erro": str(e)}, 400
    finally:
        session.close()