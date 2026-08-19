from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from schemas import ProdutoCreate, ProdutoResponse
from fastapi import HTTPException
from models import PetDB
from schemas import PetCreate, PetResponse
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

    # DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

    # PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db:
Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto

# daqui é o PETs agora, da atividade prática 

@app.get('/pets', response_model=list[PetResponse])
def listar_pets(db: Session = Depends(get_db)):
    return db.query(PetDB).all()

# GET /pets/{id} -> retorna um único pet pelo id
@app.get('/pets/{pet_id}', response_model=PetResponse)
def obter_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
    return pet

    # DELETE /pets/{id} -> remove um pet do banco de dados
@app.delete('/pets/{pet_id}', status_code=204)
def remover_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
    db.delete(pet)
    db.commit()

@app.post('/pets', response_model=PetResponse, status_code=201)
def criar_pet(pet: PetCreate, db: Session = Depends(get_db)):
    novo_pet = PetDB(**pet.dict())
    db.add(novo_pet)
    db.commit()
    db.refresh(novo_pet)
    return novo_pet

    # PUT /pets/{id} -> atualiza um pet existente no banco
@app.put('/pets/{pet_id}', response_model=PetResponse)
def atualizar_pet(pet_id: int, dados: PetCreate, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
    pet.nome = dados.nome
    pet.especie = dados.especie
    pet.raca = dados.raca
    pet.idade = dados.idade
    db.commit()
    db.refresh(pet)
    return pet