import db
from sqlalchemy import Column, VARCHAR, Integer, Float

# ORM
class ProdutoDB(db.Base):
    __tablename__ = 'tb_produto'
    
    id_produto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    descricao = Column(VARCHAR(255), nullable=False)
    valorun = Column(Float, nullable=False)

    def __init__(self, id_produto, nome, descricao, valorun):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.valorun = valorun
