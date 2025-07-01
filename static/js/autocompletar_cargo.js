document.addEventListener('DOMContentLoaded', function () {
    const cedulaInput = document.getElementById('id_cedula');
    const origenInput = document.getElementById('id_origen');

    if (cedulaInput && origenInput) {
        cedulaInput.addEventListener('keyup', function () {
            const cedula = cedulaInput.value;
            const origen = origenInput.value;

            if (cedula.length >= 6 && origen) {
                fetch(`/consultar-cargo/?cedula=${cedula}&origen=${encodeURIComponent(origen)}`)
                .then(response => response.json())
                    .then(data => {
                        if (data.cargo) {
                            const cargoInput = document.getElementById('id_cargo');
                            const nombreInput = document.getElementById('id_nombres_apellidos');
                            if (cargoInput) {
                                cargoInput.value = data.cargo;
                            }
                            if (nombreInput) {
                                nombreInput.value = data.nombre_apellido;
                            }
                        }
                    });
            }
        });
    }
});
