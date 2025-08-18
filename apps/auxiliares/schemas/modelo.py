from ninja import Schema


class ModeloOut(Schema):
    id: int
    descripcion: str
    marca: str   # nombre legible de la marca
