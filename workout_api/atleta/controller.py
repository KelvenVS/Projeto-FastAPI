from datetime import datetime
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, Query, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
router = APIRouter()

@router.post(
    path='/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    #Verifica a existência de Categoria
    categoria_name = atleta_in.categoria.nome
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Categoria {categoria_name} não foi encontrada.")
    
    #Verifica a existência do Centro de Treinamento
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Centro de Treinamento {centro_treinamento} não foi encontrado.")
    
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocorreu um erro ao inserir os dados no banco.")
    
    return atleta_out

@router.get(
    path='/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def get_all_atleta(db_session: DatabaseDependency,) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    path='/by_id_cpf_nome',
    summary='Consultar um atleta pelo id, nome ou cpf',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_atleta_by_id_name_cpf(
    db_session: DatabaseDependency,
    id: Optional[UUID4] = Query(None, description="Filtrar pelo id do atleta"),
    nome: Optional[str] = Query(None, description="Filtrar pelo nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar pelo CPF do atleta"),
) -> AtletaOut:
    query = select(AtletaModel)
    
    if not id and not nome and not cpf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Nenhum filtro aplicado")
    
    filters_applied = []  # Lista para armazenar os filtros aplicados
        
    # Se o id foi fornecido, adiciona o filtro pelo id
    if id:
        query = query.filter(AtletaModel.id == id)
        filters_applied.append(f"id = {id}")

    # Se o nome foi fornecido, adiciona o filtro no nome
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
        filters_applied.append(f"nome = {nome}")
        
    # Se o CPF foi fornecido, adiciona o filtro no CPF
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)
        filters_applied.append(f"cpf = {cpf}")

    # Executando a consulta
    result = await db_session.execute(query)
    atleta = result.scalars().first() 
    
    if not atleta:
        filters_str = ", ".join(filters_applied)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado {filters_str}")
    
    return atleta

@router.patch(
    path='/{id}',
    summary='Editar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def update_atleta(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...),) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(
    path='/{id}',
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_atleta(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado pelo id: {id}")
    
    await db_session.delete(atleta)
    await db_session.commit()