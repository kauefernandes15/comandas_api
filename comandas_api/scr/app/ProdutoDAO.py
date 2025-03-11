from fastapi import APIRouter
from domain.entities.Produto import Produto
import db
from infra.orm.ProdutoModel import ProdutoDB

router = APIRouter()

# Rota para buscar todos os produtos
@router.get("/produto/", tags=["Produto"])
async def get_produto():
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).all()
        return {"dados": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para buscar um produto específico pelo ID
@router.get("/produto/{id}", tags=["Produto"])
async def get_produto(id: int):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).all()
        return {"dados": dados}, 200
    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para adicionar um novo produto
@router.post("/produto/", tags=["Produto"])
async def post_produto(corpo: Produto):
    try:
        session = db.Session()
        dados = ProdutoDB(None, corpo.nome, corpo.descricao, corpo.valorun)
        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para atualizar um produto existente
@router.put("/produto/{id}", tags=["Produto"])
async def put_produto(id: int, corpo: Produto):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        dados.nome = corpo.nome
        dados.descricao = corpo.descricao
        dados.valorun = corpo.valorun
        session.add(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

# Rota para excluir um produto pelo ID
@router.delete("/produto/{id}", tags=["Produto"])
async def delete_produto(id: int):
    try:
        session = db.Session()
        dados = session.query(ProdutoDB).filter(ProdutoDB.id_produto == id).one()
        session.delete(dados)
        session.commit()
        return {"id": dados.id_produto}, 200
    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()
