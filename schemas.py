# schemas.py
from pydantic import BaseModel
class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
# PARTE DOS PETS EM!!!
class PetBase(BaseModel):
    nome: str
    especie: str
    idade: int

class PetCreate(PetBase):
    raca: str

class PetResponse(PetBase):
    id: int

class Config:
    from_attributes = True