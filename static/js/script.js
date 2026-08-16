const formulario = document.getElementById("formulario");
const lista = document.getElementById("lista");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");
// =======================
// SERVICIOS DINÁMICOS
// =======================

const servicios = [

    {
        nombre: "Registro Académico",
        descripcion: "Administración eficiente de registros estudiantiles."
    },

    {
        nombre: "Consulta Estudiantil",
        descripcion: "Acceso rápido a información académica y reportes."
    },

    {
        nombre: "Seguimiento Académico",
        descripcion: "Monitoreo continuo del desempeño estudiantil."
    }

];

function mostrarServicios() {

    const contenedor = document.getElementById("contenedorServicios");

    let html = "";

    servicios.forEach(servicio => {

        html += `
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-body">
                    <h5>${servicio.nombre}</h5>
                    <p>${servicio.descripcion}</p>
                </div>
            </div>
        </div>
        `;

    });

    contenedor.innerHTML = html;

}
const nombre = document.getElementById("nombre");
const carrera = document.getElementById("carrera");
const semestre = document.getElementById("semestre");

let total = 0;

// =======================
// EVENTOS
// =======================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

carrera.addEventListener("input", validarCarrera);
carrera.addEventListener("blur", validarCarrera);

semestre.addEventListener("input", validarSemestre);
semestre.addEventListener("blur", validarSemestre);

formulario.addEventListener("submit", registrarEstudiante);

// =======================
// VALIDACIONES
// =======================

function validarNombre() {

    const error = document.getElementById("errorNombre");

    if (nombre.value.trim() === "") {

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        error.textContent = "El nombre es obligatorio.";

        return false;
    }

    if (nombre.value.trim().length < 3) {

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        error.textContent = "Debe tener mínimo 3 caracteres.";

        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    error.textContent = "";

    return true;

}

function validarCarrera() {

    const error = document.getElementById("errorCarrera");

    if (carrera.value.trim() === "") {

        carrera.classList.remove("is-valid");
        carrera.classList.add("is-invalid");

        error.textContent = "La carrera es obligatoria.";

        return false;
    }

    if (carrera.value.trim().length < 3) {

        carrera.classList.remove("is-valid");
        carrera.classList.add("is-invalid");

        error.textContent = "Ingrese una carrera válida.";

        return false;
    }

    carrera.classList.remove("is-invalid");
    carrera.classList.add("is-valid");

    error.textContent = "";

    return true;

}

function validarSemestre() {

    const error = document.getElementById("errorSemestre");

    if (semestre.value.trim() === "") {

        semestre.classList.remove("is-valid");
        semestre.classList.add("is-invalid");

        error.textContent = "Ingrese el semestre.";

        return false;
    }

    semestre.classList.remove("is-invalid");
    semestre.classList.add("is-valid");

    error.textContent = "";

    return true;

}

// =======================
// REGISTRAR
// =======================

function registrarEstudiante(e){

    e.preventDefault();

    mensaje.innerHTML = "";

    if(
        !validarNombre() ||
        !validarCarrera() ||
        !validarSemestre()
    ){

        mensaje.innerHTML =
        '<div class="alert alert-danger">Corrija los errores antes de registrar.</div>';

        return;

    }

    // Mostrar spinner
    document.getElementById("spinner").style.display = "block";

    setTimeout(function(){

        document.getElementById("spinner").style.display = "none";

        total++;

        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${total}</td>
            <td>${nombre.value}</td>
            <td>${carrera.value}</td>
            <td>${semestre.value}</td>
            <td>
                <button class="btn btn-danger btn-sm eliminar">
                    Eliminar
                </button>
            </td>
        `;

        lista.appendChild(fila);

        contador.textContent = total;

        mensaje.innerHTML =
        '<div class="alert alert-success">Estudiante registrado correctamente.</div>';

        fila.querySelector(".eliminar").addEventListener("click", function(){

            fila.remove();

            total--;

            contador.textContent = total;

        });

        formulario.reset();

        nombre.classList.remove("is-valid");
        carrera.classList.remove("is-valid");
        semestre.classList.remove("is-valid");

    },1500);

}

mostrarServicios();