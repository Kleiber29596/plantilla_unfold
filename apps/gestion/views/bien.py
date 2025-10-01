# apps/bienes/api/views.py

from typing import List
from ninja import Router
from apps.gestion.schemas.bien import BienIn, BienOut, BienPatch, BienListOut, BienSchemaOut
from apps.gestion.models.bien import Bien
from django.shortcuts import get_object_or_404
from apps.auxiliares.models.modelo import Modelo
from apps.auxiliares.models.categoria import Categoria, Subcategoria
from django.db import transaction
from ninja.errors import HttpError
from django.db.models import Q


router = Router(tags=["Bienes"])


# apps/bienes/api/router.py
@router.get("/listar", response=BienListOut)
def listar_bienes(request, page: int = 1, page_size: int = 10, q: str = ""):
    page = max(1, page)
    page_size = min(max(1, page_size), 100)

    qs = (Bien.objects
              .select_related("categoria", "subcategoria", "modelo")  # 👈 Añadir subcategoria
              .order_by("-id"))

    if q:
        qs = qs.filter(
            Q(cod_bien__icontains=q) |
            Q(estatus__icontains=q) |
            Q(condicion__icontains=q) |
            Q(categoria__descripcion__icontains=q) |
            Q(subcategoria__descripcion__icontains=q) | # 👈 Añadir subcategoria al filtro
            Q(modelo__descripcion__icontains=q)
        )

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size

    # ⚠️ IMPORTANTE: convierte a lista antes de mapear (evita "DjangoGetter")
    page_items = list(qs[start:end])
    items = [bien_to_out(b) for b in page_items]

    return {"results": items, "total": total}



@router.post("/crear", response=BienSchemaOut)
def crear_bien(request, payload: BienIn):
    categoria = get_object_or_404(Categoria, id=payload.categoria_id)
    subcategoria = get_object_or_404(Subcategoria, id=payload.subcategoria_id) # 👈 Obtener Subcategoria

    modelo = None
    if payload.modelo_id:
        modelo = get_object_or_404(Modelo, id=payload.modelo_id)

    bien = Bien.objects.create(
        categoria=categoria,
        subcategoria=subcategoria, # 👈 Añadir subcategoria
        modelo=modelo,
        caracteristicas=payload.caracteristicas,
        cod_bien=payload.cod_bien,
        tipo_uso=payload.tipo_uso,
        valor_unitario=payload.valor_unitario,
        condicion=payload.condicion,
        estatus=payload.estatus,
        fecha_adquisicion=payload.fecha_adquisicion,
    )

    return BienSchemaOut(
        id=bien.id,
        cod_bien=bien.cod_bien,
        categoria=str(bien.categoria),
        subcategoria=str(bien.subcategoria), # 👈 Añadir subcategoria
        modelo=str(bien.modelo) if bien.modelo else None,
        tipo_uso=bien.tipo_uso,
        valor_unitario=bien.valor_unitario,
        condicion=bien.condicion,
        estatus=bien.estatus,
        fecha_adquisicion=bien.fecha_adquisicion,
    )



def bien_to_out(bien: Bien) -> BienOut:
    """
    Mapea el modelo Bien a BienOut mostrando nombres de relaciones
    (lo que tu tabla espera).
    """
    categoria_txt = bien.categoria.descripcion if bien.categoria_id else ""
    subcategoria_txt = bien.subcategoria.descripcion if bien.subcategoria_id else "" # 👈 Añadir subcategoria_txt
    # Puedes enriquecer el modelo, p.ej. incluir marca:
    modelo_txt = None
    if bien.modelo_id:
        try:
            modelo_txt = bien.modelo.descripcion  # o f"{bien.modelo.descripcion} - {bien.modelo.marca}"
        except Exception:
            modelo_txt = None

    return BienSchemaOut(
        id=bien.id,
        cod_bien=bien.cod_bien,
        categoria=categoria_txt,
        subcategoria=subcategoria_txt, # 👈 Añadir subcategoria
        modelo=modelo_txt,
        tipo_uso=bien.tipo_uso,
        valor_unitario=float(bien.valor_unitario),
        condicion=bien.condicion,
        estatus=bien.estatus,
        fecha_adquisicion=bien.fecha_adquisicion,
    )


@router.put("editar/{bien_id}", response=BienOut)
@transaction.atomic
def actualizar_bien(request, bien_id: int, payload: BienIn):
    """
    Actualización TOTAL del Bien (PUT).
    Requiere todos los campos de BienIn.
    """
    try:
        bien = Bien.objects.select_for_update().get(id=bien_id)
    except Bien.DoesNotExist:
        raise HttpError(404, "Bien no encontrado")

    # Validar y obtener FKs: Categoria y Subcategoria (requeridas) y Modelo (opcional)
    try:
        categoria = Categoria.objects.get(id=payload.categoria_id)
        subcategoria = Subcategoria.objects.get(id=payload.subcategoria_id) # 👈 Obtener Subcategoria
    except Categoria.DoesNotExist:
        raise HttpError(400, "Categoría inválida")
    except Subcategoria.DoesNotExist:
        raise HttpError(400, "Subcategoría inválida")

    modelo = None
    if payload.modelo_id is not None:
        try:
            modelo = Modelo.objects.get(id=payload.modelo_id)
        except Modelo.DoesNotExist:
            raise HttpError(400, "Modelo inválido")

    # Asignar campos
    bien.cod_bien = payload.cod_bien
    bien.categoria = categoria
    bien.subcategoria = subcategoria # 👈 Asignar Subcategoria
    bien.modelo = modelo  # puede ser None
    bien.tipo_uso = payload.tipo_uso
    bien.valor_unitario = payload.valor_unitario
    bien.condicion = payload.condicion
    bien.estatus = payload.estatus
    bien.fecha_adquisicion = payload.fecha_adquisicion
    bien.caracteristicas = payload.caracteristicas or ""
    bien.save(update_fields=[
        "cod_bien", "categoria", "subcategoria", "modelo", "tipo_uso", "valor_unitario", # 👈 Añadir subcategoria
        "condicion", "estatus", "fecha_adquisicion", "caracteristicas"
    ])

    return bien_to_out(bien)

@router.patch("bienes/{bien_id}", response=BienOut)
@transaction.atomic
def actualizar_bien_parcial(request, bien_id: int, payload: BienPatch):
    """
    Actualización PARCIAL del Bien (PATCH).
    Solo aplica campos presentes en el payload.
    """
    try:
        bien = Bien.objects.select_for_update().get(id=bien_id)
    except Bien.DoesNotExist:
        raise HttpError(404, "Bien no encontrado")

    # FKs
    if payload.categoria_id is not None:
        try:
            bien.categoria = Categoria.objects.get(id=payload.categoria_id)
        except Categoria.DoesNotExist:
            raise HttpError(400, "Categoría inválida")

    if payload.subcategoria_id is not None: # 👈 Añadir lógica para subcategoria
        try:
            bien.subcategoria = Subcategoria.objects.get(id=payload.subcategoria_id)
        except Subcategoria.DoesNotExist:
            raise HttpError(400, "Subcategoría inválida")


    # Para modelo soportamos: setear un ID o "borrar" con null
    if payload.modelo_id is not None:
        if payload.modelo_id == 0 or payload.modelo_id is None:
            bien.modelo = None
        else:
            try:
                bien.modelo = Modelo.objects.get(id=payload.modelo_id)
            except Modelo.DoesNotExist:
                raise HttpError(400, "Modelo inválido")

    # Primitivos
    if payload.cod_bien is not None:
        bien.cod_bien = payload.cod_bien
    if payload.tipo_uso is not None:
        bien.tipo_uso = payload.tipo_uso
    if payload.valor_unitario is not None:
        bien.valor_unitario = payload.valor_unitario
    if payload.condicion is not None:
        bien.condicion = payload.condicion
    if payload.estatus is not None:
        bien.estatus = payload.estatus
    if payload.fecha_adquisicion is not None:
        bien.fecha_adquisicion = payload.fecha_adquisicion
    if payload.caracteristicas is not None:
        bien.caracteristicas = payload.caracteristicas

    bien.save()
    return bien_to_out(bien)