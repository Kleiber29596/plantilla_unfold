document.addEventListener('DOMContentLoaded', function() {
    // Es importante usar los IDs correctos que Django Admin asigna a los campos.
    // Generalmente son 'id_<nombre_del_campo>'.
    const estatusSelect = document.getElementById('id_estatus');
    const motivoField = document.getElementById('id_motivo');
 
    // Llamar a la función al cargar la página para establecer el estado inicial
    // Esto es útil si estás editando un objeto existente.
    if (estatusSelect && motivoField) { // Asegurarse de que los elementos existen
        toggleMotivoField();
    }
});




function toggleMotivoField() { 
    const estatusSelect = document.getElementById('id_estatus');
    const motivoField = document.getElementById('id_motivo');
    
    if (estatusSelect.value === 'Inactivo') {
        motivoField.disabled = false;
        // Opcional: Hacerlo requerido a nivel de HTML5 para validación en el cliente
        motivoField.required = true;
        console.log(estatusSelect.value)

    } else {
        motivoField.disabled = true;
        motivoField.value = ''; // Limpiar el valor si no es 'Inactivo'
        motivoField.required = false;
        console.log(estatusSelect.value)
    }
}