// js/deshabilitar_asignacion.js

(function() {
    function initializeScript() {
        if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
            // django.jQuery ya está disponible, ejecuta tu código
            (function($) {
                $(document).ready(function() {
                    console.log("Script 'deshabilitar_asignacion.js' inicializado con django.jQuery.");

                    var estatusField = $('#id_estatus');
                    console.log(estatusField);
                    // Asegúrate de que este selector sea correcto para tu HTML
                    var motivoFieldRow = $('.form-group.field-motivo'); // <--- AHORA CON form-group

                    if (estatusField.length === 0) {
                        console.error("Campo 'estatus' (#id_estatus) no encontrado. Verifica el ID en el HTML.");
                        return;
                    }
                    if (motivoFieldRow.length === 0) {
                        console.warn("Fila del campo 'motivo' (.form-group.field-motivo) no encontrada. VERIFICA EL NOMBRE DEL CAMPO Y CLASE EN EL HTML.");
                        // No salimos, es un warning que nos dice que no lo encontró
                    }

                    function toggleMotivoField() {
                        var currentStatus = estatusField.val();
                        console.log("Estatus actual:", currentStatus);
                        if (currentStatus === 'Activo') {
                            motivoFieldRow.hide();
                            console.log("Estatus es 'Activo'. Ocultando campo 'motivo'.");
                        } else {
                            motivoFieldRow.show();
                            console.log("Estatus NO es 'Activo'. Mostrando campo 'motivo'.");
                        }
                    }

                    toggleMotivoField(); // Ejecuta al cargar para establecer el estado inicial

                    estatusField.change(function() {
                        console.log("Cambio detectado en campo 'estatus'.");
                        toggleMotivoField();
                    });
                });
            })(django.jQuery);
        } else {
            // django.jQuery aún no está disponible, intenta de nuevo después de un breve retardo
            console.warn("django.jQuery aún no está disponible. Reintentando...");
            setTimeout(initializeScript, 50); // Intenta de nuevo en 50ms
        }
    }

    // Inicia el proceso de inicialización
    initializeScript();
})();