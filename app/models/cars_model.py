from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, String, Integer, Boolean

from app.configs.database import db


@dataclass
class Cars(db.Model):
    id: str
    marca: str
    modelo: str
    valor: int
    ano: int
    km: int
    cidade: str
    estado: str
    foto: str
    vendido: bool
    promocao: bool

    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    marca = Column(String(127), nullable=False)
    modelo = Column(String(127), nullable=False)
    valor = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    km = Column(Integer, nullable=False)
    cidade = Column(String(127), nullable=False)
    estado = Column(String(127), nullable=False)
    foto = Column(String(127), nullable=False)
    vendido = Column(Boolean, default=False)
    promocao = Column(Boolean, default=False)
