from workout_api.contrib.schemas import BaseSchema
from typing import Annotated
from pydantic import Field, PositiveFloat

class Categorias(BaseSchema):
    nome: Annotated[str, Field(description='Categoria', example='Scale', max_length=10)]