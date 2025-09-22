from apps.gestion.models.prestamo    import Prestamo, DetallePrestamo
from apps.gestion.schemas.prestamos  import PrestamoIn, PrestamoOut, DetallePrestamoOut, DetallePrestamoIn
from ninja                           import Router
from typing                          import List
from django.shortcuts import get_object_or_404



router = Router(tags=["Préstamos"])

@router.post("/", response={200: dict})
def create_prestamo(request, data: PrestamoIn):
    try:
        prestamo = Prestamo.objects.create(
            fecha_inicio=data.fecha_inicio,
            fecha_final=data.fecha_final,
            encargado=data.encargado,
            ubicacion_departamento_id=data.ubicacion_departamento_id,
            motivo_id=data.motivo_id,
        )

        for bien in data.bienes:
            DetallePrestamo.objects.create(
                prestamo=prestamo,
                bien_id=bien.bien_id
            )

        return {"message": "Préstamo registrado con éxito", "id": prestamo.id}

    except Exception as e:
        return  {"error": str(e)}


@router.get("/listar", response=List[PrestamoOut])
def list_prestamos(request):
    try:
        # traer relaciones eficientemente
        prestamos_qs = (
            Prestamo.objects
            .select_related("ubicacion_departamento", "motivo")
            .prefetch_related("detalles__bien")
            .all()
        )

        result = []
        for p in prestamos_qs:
            detalles_list = []
            # usar el related_name definido: "detalles"
            for d in p.detalles.all():
                bien_obj = d.bien
                detalles_list.append({
                    "id": d.id,
                    "bien_id": bien_obj.id,
                    "bien": getattr(bien_obj, "cod_bien", str(bien_obj)),
                    "condicion_devolucion": d.condicion_devolucion,
                })

            result.append({
                "id": p.id,
                "fecha_inicio": p.fecha_inicio,
                "fecha_final": p.fecha_final,
                "encargado": p.encargado,
                "ubicacion_departamento": str(p.ubicacion_departamento) if p.ubicacion_departamento else None,
                "motivo": p.motivo.descripcion if p.motivo else None,
                "fecha_devolucion": p.fecha_devolucion,
                "status": p.status,
                "detalles": detalles_list,
            })

        return result

    except Exception as e:
        # evita 500s crípticos: devuelve error legible para debug
        raise HttpError(500, f"Error al listar préstamos: {e}")


@router.get("/{prestamo_id}", response=PrestamoOut)
def ver_prestamo(request, prestamo_id: int):
    prestamo = get_object_or_404(
        Prestamo.objects.prefetch_related("detalles__bien", "ubicacion_departamento", "motivo"),
        id=prestamo_id
    )
    return prestamo


@router.put("/{prestamo_id}/devolucion", response=PrestamoOut)
def marcar_prestamo_devuelto(request, prestamo_id: int):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    prestamo.marcar_devuelto()
    return prestamo


@router.put("/detalle/{detalle_id}/devolucion", response=DetallePrestamoOut)
def marcar_detalle_devuelto(request, detalle_id: int, condicion: str):
    detalle = get_object_or_404(DetallePrestamo, id=detalle_id)
    detalle.condicion_devolucion = condicion
    detalle.save()
    return {
        "id": detalle.id,
        "bien_id": detalle.bien.id,
        "bien": str(detalle.bien),   # o el campo que uses, ej: detalle.bien.cod_bien
        "condicion_devolucion": detalle.condicion_devolucion,
    }

