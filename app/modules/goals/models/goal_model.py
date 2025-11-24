from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class GoalModel(Base):
    __tablename__ = "metas"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuarios: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    texto: Mapped[str] = mapped_column(String(100), nullable=False)