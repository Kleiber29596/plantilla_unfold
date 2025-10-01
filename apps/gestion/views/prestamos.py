from apps.gestion.models.prestamo    import Prestamo, DetallePrestamo, ResponsablePrestamo
from apps.gestion.schemas.prestamos  import PrestamoIn, PrestamoOut, DetallePrestamoOut, DetallePrestamoIn, ResponsablePrestamoIn
from ninja                           import Router
from typing                          import List
from django.shortcuts                import get_object_or_404
from ninja.errors                    import HttpError
from ninja.responses import Response
from apps.gestion.views.acta_prestamo import ActaPrestamoService
from django.http import HttpResponse
from apps.gestion.schemas.prestamos import ResponsablePrestamoOut

router = Router(tags=["Préstamos"])

@router.post("/", response={200: dict})
def create_prestamo(request, data: PrestamoIn):
    try:
        prestamo = Prestamo.objects.create(
            fecha_inicio=data.fecha_inicio,
            fecha_final=data.fecha_final,
            departamento_entrega_id=data.departamento_entrega_id,
            departamento_recibe_id=data.departamento_recibe_id,
            motivo_id=data.motivo_id,
        )

        for bien in data.bienes:
            DetallePrestamo.objects.create(
                prestamo=prestamo,
                bien_id=bien.bien_id
            )
        for responsable in data.responsables:
            ResponsablePrestamo.objects.create(
                prestamo=prestamo,
                responsable_id=responsable
                
            )

        return {"message": "Préstamo registrado con éxito", "id": prestamo.id}

    except Exception as e:
        return  {"error": str(e)}

@router.get("/listar", response=List[PrestamoOut])
def list_prestamos(request):
    try:
        prestamos_qs = (
            Prestamo.objects
            .select_related("departamento_entrega", "departamento_recibe", "motivo")
            .prefetch_related("detalles__bien", "responsables__responsable__persona")
            .all()
        )

        result = []
        for p in prestamos_qs:
            # --- Detalles ---
            detalles_list = []
            for d in p.detalles.all():
                detalles_list.append({
                    "id": d.id,
                    "bien":d.bien,   # 👈 aquí mejor convertir a string para evitar problemas
                    "condicion_devolucion": d.condicion_devolucion,
                })

            responsables_list = []
            for r in p.responsables.all():
                responsables_list.append({
                    "id": r.id,
                    "rol": r.rol,
                    "persona": {
                        "id": r.responsable.persona.id,
                        "cedula": r.responsable.persona.cedula,
                        "nombres_apellidos": r.responsable.persona.nombres_apellidos,
                    }
                })

            result.append({
                    "id": p.id,
                    "fecha_inicio": p.fecha_inicio,
                    "fecha_final": p.fecha_final,
                    "departamento_entrega": str(p.departamento_entrega) if p.departamento_entrega else None,
                    "departamento_recibe": str(p.departamento_recibe) if p.departamento_recibe else None,
                    "motivo": p.motivo.descripcion if p.motivo else None,
                    "fecha_devolucion": p.fecha_devolucion,
                    "status": p.status,
                    "detalles": detalles_list,
                    "responsables": responsables_list,  # 👈 ahora es lista, como lo espera el schema
                })

        return result

    except Exception as e:
        raise HttpError(500, f"Error al listar préstamos: {e}")



@router.get("/{prestamo_id}", response=PrestamoOut)
def ver_prestamo(request, prestamo_id: int):
    prestamo = get_object_or_404(
        Prestamo.objects.prefetch_related("detalles__bien", "departamento_entrega", "departamento_recibe" "motivo"),
        id=prestamo_id
    )
    return prestamo



@router.put("/{prestamo_id}/devolucion")
def marcar_prestamo_devuelto(request, prestamo_id: int):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    prestamo.marcar_devuelto()
    return Response({"message": "Préstamo devuelto con éxito"}, status=200)



@router.put("/detalle/{detalle_id}/devolucion", response=DetallePrestamoOut)
def marcar_detalle_devuelto(request, detalle_id: int, condicion: str):
    detalle = get_object_or_404(DetallePrestamo, id=detalle_id)
    detalle.condicion_devolucion = condicion
    detalle.save()
    return detalle   # 👈 igual aquí


@router.get("/prestamos/{prestamo_id}/acta", response=None)
def generar_acta_prestamo(request, prestamo_id: int):
    """
    Endpoint para generar y descargar el PDF del Acta de Préstamo.
    """

    # Traer el préstamo optimizando consultas
    prestamo = get_object_or_404(
        Prestamo.objects
        .select_related('ubicacion_departamento')  # traer dependencia
        .prefetch_related('detalles__bien'),      # traer detalles y sus bienes
        id=prestamo_id
    )

    # Preparar la respuesta HTTP con PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="acta_prestamo_{prestamo.id}.pdf"'

    # Crear servicio y generar PDF
    service = ActaPrestamoService(prestamo)
    service.generar_pdf(response)

    return response


# ---------- Schemas de ResponsablesPréstamos ----------
@router.post("/registrar_responsables", response={201: ResponsablePrestamoOut})
def create_responsables(request, data: ResponsablePrestamoIn):
    prestamo_id = data.prestamo_id

    entrega = ResponsablePrestamo.objects.create(
        prestamo_id=prestamo_id, responsable_id=data.responsables.entrega
    )
    recibe = ResponsablePrestamo.objects.create(
        prestamo_id=prestamo_id, responsable_id=data.responsables.recibe
    )
    testigo_entrega = ResponsablePrestamo.objects.create(
        prestamo_id=prestamo_id, responsable_id=data.responsables.testigo_entrega
    )
    testigo_recibe = ResponsablePrestamo.objects.create(
        prestamo_id=prestamo_id, responsable_id=data.responsables.testigo_recibe
    )

    return {
        "id": entrega.id,  # o el id de alguno de los creados
        "prestamo_id": prestamo_id,
        "entrega_id": entrega.responsable_id,
        "recibe_id": recibe.responsable_id,
        "testigo_entrega_id": testigo_entrega.responsable_id,
        "testigo_recibe_id": testigo_recibe.responsable_id,
    }


@router.get("/listar/{prestamo_id}", response=List[ResponsablePrestamoOut])
def listar_responsables_prestamo(request, prestamo_id: int):
    responsables = ResponsablePrestamo.objects.filter(prestamo_id=prestamo_id)
    return responsables

