import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Optional, Literal
from src.schemas.reserva import Reserva, TipoReserva
from src.schemas.avaliacao import Avaliacao, getDB as getAvaliacaoDB
import json

app = FastAPI()
router = APIRouter()

UF_SIGLAS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

def getDB():
    try:
        print("Tentando carregar o banco de dados...")
        with open(os.path.join(os.path.dirname(__file__), '../db/db_reservas.json'), 'r') as dbu:
            db = json.load(dbu)
        print("Banco de dados carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao carregar o banco de dados")
    
    # Calcular avaliações médias
    avaliacoes = getAvaliacaoDB()
    for reserva in db["reservas"]:
        endereco = reserva['endereco']
        notas = [avaliacao['nota'] for avaliacao in avaliacoes if avaliacao['endereco'] == endereco]
        if notas:
            reserva['avalMedia'] = sum(notas) / len(notas)
        else:
            reserva['avalMedia'] = 0
    
    return db["reservas"]

def saveDB(db):
    try:
        with open(os.path.join(os.path.dirname(__file__), '../db/db_reservas.json'), 'w') as dbu:
            json.dump(db, fp=dbu, indent=4)
    except Exception as e:
        print(f"Erro ao salvar o banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar o banco de dados")
    return db

@router.get("/reservas")
async def reservas(
    tipo: Optional[Literal['Quarto', 'Casa', 'Apartamento', 'Salão']] = None,
    petfriendly: Optional[bool] = None,
    uf: Optional[Literal[
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
        'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]] = None,
    valmax: Optional[int] = None,
    valmin: Optional[int] = None,
    avaliacao: Optional[Literal['1', '2', '3', '4', '5']] = None,
    destacado: Optional[bool] = None
) -> List[Reserva]:
    try:
        print("Recebendo requisição para /reservas...")
        db_reservas = getDB()
        print(f"Reservas carregadas: {db_reservas}")
        reserva_list = [Reserva(**b) for b in db_reservas]
        print(f"Reservas processadas: {reserva_list}")
    except Exception as e:
        print(f"Erro ao processar reservas: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar reservas")

    if tipo: 
        if tipo not in TipoReserva.__members__.values():
            raise HTTPException(status_code=400, detail="Tipo de reserva inválido")
        reserva_list = [b for b in reserva_list if b.tipo.lower() == tipo.lower()]
    if petfriendly is not None:
        reserva_list = [b for b in reserva_list if b.petfriendly == petfriendly]
    if uf:
        if uf.upper() not in UF_SIGLAS:
            raise HTTPException(status_code=400, detail="UF inválido")
        reserva_list = [b for b in reserva_list if b.endereco.split(",")[-1].strip().upper() == uf.upper()]
    if valmax:
        reserva_list = [b for b in reserva_list if b.preco <= valmax]
    if valmin:
        reserva_list = [b for b in reserva_list if b.preco >= valmin]
    if avaliacao:
        reserva_list = [b for b in reserva_list if b.avalMedia >= float(avaliacao)]
    if destacado is not None:
        reserva_list = [b for b in reserva_list if b.destacado == destacado]

    if not reserva_list:
        raise HTTPException(status_code=404, detail="Nenhuma reserva encontrada dentro desses filtros")

    return reserva_list

@router.get("/reservas/{reserva_name}")
async def get_reserva(reserva_name: str) -> Reserva:
    try:
        db_reservas = getDB()
        for reserva in db_reservas:
            if reserva['titulo'].lower().replace(" ", "-") == reserva_name:
                return Reserva(**reserva)
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    except Exception as e:
        print(f"Erro ao buscar reserva: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar reserva")

@router.get("/avaliacoes/{reserva_name}")
async def get_avaliacoes(reserva_name: str) -> List[Avaliacao]:
    try:
        db_reservas = getDB()
        for reserva in db_reservas:
            if reserva['titulo'].lower().replace(" ", "-") == reserva_name:
                endereco = reserva['endereco']
                break
        else:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")

        avaliacoes = getAvaliacaoDB()
        avaliacoes_reserva = [Avaliacao(**avaliacao) for avaliacao in avaliacoes if avaliacao['endereco'] == endereco]

        return avaliacoes_reserva
    except Exception as e:
        print(f"Erro ao buscar avaliações: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar avaliações")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)