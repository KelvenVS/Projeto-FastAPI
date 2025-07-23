from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String

class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)