# apps/bienes/api/schemas.py
from ninja import Schema
from datetime import date
from typing import Optional, List

class CategoriaOut(Schema):
    id: int
    descripcion: str

    class Config:
        from_attributes = True  # 👈 permite mapear directamente objetos Django


class SubcategoriaOut(Schema):
    id: int
    descripcion: str

    class Config:
        from_attributes = True


class ModeloOut(Schema):
    id: int
    descripcion: str

    class Config:
        from_attributes = True


# ---------- Schema de Bien ----------

class BienOut(Schema):
    id: int
    cod_bien: str
    categoria: CategoriaOut
    subcategoria: SubcategoriaOut
    modelo: ModeloOut
    tipo_uso: str
    valor_unitario: float
    condicion: str
    estatus: str
    fecha_adquisicion: date

    class Config:
        from_attributes = True
        



class BienSchemaOut(Schema):
    id: int
    cod_bien: str
    categoria: Optional[str]
    subcategoria: Optional[str]
    modelo: Optional[str]
    tipo_uso: Optional[str]
    valor_unitario: float
    condicion: str
    estatus: str
    fecha_adquisicion: date
    caracteristicas: Optional[str] = None




class BienIn(Schema):
    categoria_id: int
    subcategoria_id: int
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
    subcategoria_id: Optional[int] = None
    modelo_id: Optional[int] = None
    caracteristicas: Optional[str] = None
    cod_bien: Optional[str] = None
    tipo_uso: Optional[str] = None
    valor_unitario: Optional[float] = None
    condicion: Optional[str] = None
    estatus: Optional[str] = None
    fecha_adquisicion: Optional[date] = None



class BienListOut(Schema):
    results: List[BienSchemaOut]
    total: int