from ninja import Schema

class CategoriaOut(Schema):
    id: int
    descripcion: str

class SubcategoriaOut(Schema):
    id: int
    descripcion: str
    categoria_id: int  # Relación con Categoria

