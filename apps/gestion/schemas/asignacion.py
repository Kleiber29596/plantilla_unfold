# apps/bienes/api/schemas.py
from ninja import Schema
from datetime import date
from typing import Optional, List

class BienOut(Schema):
    id: int
    bien: str
    : str
    modelo: str | None
    tipo_uso: str
    valor_unitario: float
    condicion: str
    estatus: str
    fecha_adquisicion: date


class BienIn(Schema):
    categoria_id: int
    modelo_id: Optional[int] = None
    caracteristicas: Optional[str] = None
    cod_bien: str
    tipo_uso: str
    valor_unitario: float
    condicion: str
    estatus: str
    fecha_adquisicion: date


class BienPatch(Schema):
    categoria_id: Optional[int] = None
    modelo_id: Optional[int] = None
    caracteristicas: Optional[str] = None
    cod_bien: Optional[str] = None
    tipo_uso: Optional[str] = None
    valor_unitario: Optional[float] = None
    condicion: Optional[str] = None
    estatus: Optional[str] = None
    fecha_adquisicion: Optional[date] = None



class BienListOut(Schema):
    results: List[BienOut]
    total: int