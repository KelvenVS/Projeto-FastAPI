from workout_api.contrib.schemas import BaseSchema
from typing import Annotated
from pydantic import UUID4, Field, PositiveFloat

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Categoria', example='Scale', max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador')]