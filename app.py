from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def siguiente_id(lista):
    """
    Obtiene un ID nuevo sin repetir IDs existentes.
    """
    if not lista:
        return 1

    return max(item["id"] for item in lista) + 1


def buscar_producto_por_nombre(nombre):
    """
    Busca un producto por su nombre.
    """
    return next(
        (p for p in productos_lista if p["nombre"] == nombre),
        None
    )


# =========================================================
# PRODUCTOS
# =========================================================

productos_lista = [
    {
        "id": 1,
        "nombre": "Registro Académico",
        "descripcion": "Administración de estudiantes",
        "precio": 25.00
    },
    {
        "id": 2,
        "nombre": "Consulta Estudiantil",
        "descripcion": "Consulta de información académica",
        "precio": 15.00
    },
    {
        "id": 3,
        "nombre": "Seguimiento Académico",
        "descripcion": "Seguimiento del desempeño estudiantil",
        "precio": 20.00
    },
    {
        "id": 4,
        "nombre": "Certificado Académico",
        "descripcion": "Emisión de certificados para estudiantes",
        "precio": 10.00
    }
]


# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def inicio():
    return render_template("index.html")


# =========================================================
# MÓDULO PRODUCTOS
# =========================================================

@app.route("/productos")
def productos():
    return render_template(
        "productos.html",
        productos=productos_lista
    )


# ---------------------------------------------------------
# AGREGAR PRODUCTO
# ---------------------------------------------------------

@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = float(request.form["precio"])

        nuevo_producto = {
            "id": siguiente_id(productos_lista),
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio
        }

        productos_lista.append(nuevo_producto)

        return redirect("/productos")

    return render_template("agregar_producto.html")


# ---------------------------------------------------------
# EDITAR PRODUCTO
# ---------------------------------------------------------

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    producto = next(
        (p for p in productos_lista if p["id"] == id),
        None
    )

    if producto is None:
        return "Producto no encontrado"

    if request.method == "POST":

        producto["nombre"] = request.form["nombre"]
        producto["descripcion"] = request.form["descripcion"]
        producto["precio"] = float(request.form["precio"])

        return redirect("/productos")

    return render_template(
        "editar_producto.html",
        producto=producto
    )


# ---------------------------------------------------------
# ELIMINAR PRODUCTO
# ---------------------------------------------------------

@app.route("/eliminar_producto/<int:id>")
def eliminar_producto(id):

    global productos_lista

    productos_lista = [
        p for p in productos_lista
        if p["id"] != id
    ]

    return redirect("/productos")


# =========================================================
# CLIENTES
# =========================================================

clientes_lista = [
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "correo": "juan@gmail.com",
        "estado": "Activo"
    },
    {
        "id": 2,
        "nombre": "María López",
        "correo": "maria@gmail.com",
        "estado": "Activo"
    },
    {
        "id": 3,
        "nombre": "Carlos Sánchez",
        "correo": "carlos@gmail.com",
        "estado": "Inactivo"
    }
]


# ---------------------------------------------------------
# LISTA DE CLIENTES
# ---------------------------------------------------------

@app.route("/clientes")
def clientes():
    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


# ---------------------------------------------------------
# AGREGAR CLIENTE
# ---------------------------------------------------------

@app.route("/agregar_cliente", methods=["GET", "POST"])
def agregar_cliente():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        estado = request.form["estado"]

        nuevo_cliente = {
            "id": siguiente_id(clientes_lista),
            "nombre": nombre,
            "correo": correo,
            "estado": estado
        }

        clientes_lista.append(nuevo_cliente)

        return redirect("/clientes")

    return render_template("agregar_cliente.html")


# ---------------------------------------------------------
# EDITAR CLIENTE
# ---------------------------------------------------------

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):

    cliente = next(
        (c for c in clientes_lista if c["id"] == id),
        None
    )

    if cliente is None:
        return "Cliente no encontrado"

    if request.method == "POST":

        cliente["nombre"] = request.form["nombre"]
        cliente["correo"] = request.form["correo"]
        cliente["estado"] = request.form["estado"]

        return redirect("/clientes")

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


# ---------------------------------------------------------
# ELIMINAR CLIENTE
# ---------------------------------------------------------

@app.route("/eliminar_cliente/<int:id>")
def eliminar_cliente(id):

    global clientes_lista

    clientes_lista = [
        cliente
        for cliente in clientes_lista
        if cliente["id"] != id
    ]

    return redirect("/clientes")


# =========================================================
# PROVEEDORES
# =========================================================

proveedores_lista = [
    {
        "id": 1,
        "nombre": "Proveedor Amazonía",
        "correo": "amazonia@gmail.com",
        "telefono": "0991234567",
        "estado": "Activo"
    },
    {
        "id": 2,
        "nombre": "Distribuidora Nacional",
        "correo": "distribuidora@gmail.com",
        "telefono": "0987654321",
        "estado": "Activo"
    },
    {
        "id": 3,
        "nombre": "Servicios Académicos",
        "correo": "servicios@gmail.com",
        "telefono": "0974561238",
        "estado": "Inactivo"
    }
]


# ---------------------------------------------------------
# LISTA DE PROVEEDORES
# ---------------------------------------------------------

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


# ---------------------------------------------------------
# AGREGAR PROVEEDOR
# ---------------------------------------------------------

@app.route("/agregar_proveedor", methods=["GET", "POST"])
def agregar_proveedor():

    if request.method == "POST":

        nuevo_proveedor = {
            "id": siguiente_id(proveedores_lista),
            "nombre": request.form["nombre"],
            "correo": request.form["correo"],
            "telefono": request.form["telefono"],
            "estado": request.form["estado"]
        }

        proveedores_lista.append(nuevo_proveedor)

        return redirect("/proveedores")

    return render_template("agregar_proveedor.html")


# ---------------------------------------------------------
# EDITAR PROVEEDOR
# ---------------------------------------------------------

@app.route("/editar_proveedor/<int:id>", methods=["GET", "POST"])
def editar_proveedor(id):

    proveedor = next(
        (p for p in proveedores_lista if p["id"] == id),
        None
    )

    if proveedor is None:
        return "Proveedor no encontrado"

    if request.method == "POST":

        proveedor["nombre"] = request.form["nombre"]
        proveedor["correo"] = request.form["correo"]
        proveedor["telefono"] = request.form["telefono"]
        proveedor["estado"] = request.form["estado"]

        return redirect("/proveedores")

    return render_template(
        "editar_proveedor.html",
        proveedor=proveedor
    )


# ---------------------------------------------------------
# ELIMINAR PROVEEDOR
# ---------------------------------------------------------

@app.route("/eliminar_proveedor/<int:id>")
def eliminar_proveedor(id):

    proveedor = next(
        (p for p in proveedores_lista if p["id"] == id),
        None
    )

    if proveedor:
        proveedores_lista.remove(proveedor)

    return redirect("/proveedores")


# =========================================================
# FACTURACIÓN
# =========================================================

facturas_lista = [
    {
        "id": 1,
        "cliente": "Juan Pérez",
        "producto": "Registro Académico",
        "cantidad": 1,
        "total": 25.00,
        "estado": "Pagada"
    },
    {
        "id": 2,
        "cliente": "María López",
        "producto": "Consulta Estudiantil",
        "cantidad": 2,
        "total": 30.00,
        "estado": "Pendiente"
    },
    {
        "id": 3,
        "cliente": "Carlos Sánchez",
        "producto": "Seguimiento Académico",
        "cantidad": 1,
        "total": 20.00,
        "estado": "Pagada"
    }
]


# ---------------------------------------------------------
# LISTA DE FACTURAS
# ---------------------------------------------------------

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


# ---------------------------------------------------------
# AGREGAR FACTURA
# ---------------------------------------------------------

@app.route("/agregar_factura", methods=["GET", "POST"])
def agregar_factura():

    if request.method == "POST":

        # Obtener datos del formulario
        cliente = request.form.get("cliente", "").strip()
        producto = request.form.get("producto", "").strip()

        # Cantidad
        try:
            cantidad = int(request.form.get("cantidad", 1))
        except ValueError:
            cantidad = 1

        # Evitar cantidades menores a 1
        if cantidad < 1:
            cantidad = 1

        # -------------------------------------------------
        # BUSCAR PRECIO AUTOMÁTICAMENTE
        # -------------------------------------------------

        producto_encontrado = buscar_producto_por_nombre(producto)

        if producto_encontrado:

            precio = float(producto_encontrado["precio"])

            # Total = precio del producto x cantidad
            total = precio * cantidad

        else:

            # Si por alguna razón no se encuentra el producto,
            # intentamos utilizar el total enviado por el formulario.
            try:
                total = float(request.form.get("total", 0))
            except ValueError:
                total = 0.0

        # -------------------------------------------------
        # CREAR FACTURA
        # -------------------------------------------------

        nueva_factura = {
            "id": siguiente_id(facturas_lista),
            "cliente": cliente,
            "producto": producto,
            "cantidad": cantidad,
            "total": total,
            "estado": "Pendiente"
        }

        facturas_lista.append(nueva_factura)

        return redirect("/facturacion")

    return render_template("agregar_factura.html")


# ---------------------------------------------------------
# EDITAR FACTURA
# ---------------------------------------------------------

@app.route("/editar_factura/<int:id>", methods=["GET", "POST"])
def editar_factura(id):

    factura = next(
        (f for f in facturas_lista if f["id"] == id),
        None
    )

    if factura is None:
        return "Factura no encontrada"

    if request.method == "POST":

        # -------------------------------------------------
        # DATOS DEL FORMULARIO
        # -------------------------------------------------

        cliente = request.form.get(
            "cliente",
            factura["cliente"]
        ).strip()

        producto = request.form.get(
            "producto",
            factura["producto"]
        ).strip()

        # -------------------------------------------------
        # CANTIDAD
        # -------------------------------------------------

        try:
            cantidad = int(
                request.form.get(
                    "cantidad",
                    factura["cantidad"]
                )
            )
        except ValueError:
            cantidad = factura["cantidad"]

        if cantidad < 1:
            cantidad = 1

        # -------------------------------------------------
        # BUSCAR PRECIO DEL PRODUCTO
        # -------------------------------------------------

        producto_encontrado = buscar_producto_por_nombre(producto)

        if producto_encontrado:

            precio = float(producto_encontrado["precio"])

        else:

            # Si no encuentra el producto, intenta tomar
            # el precio del formulario.
            try:
                precio = float(
                    request.form.get("precio", 0)
                )
            except ValueError:
                precio = 0.0

        # -------------------------------------------------
        # CALCULAR TOTAL
        # -------------------------------------------------

        total = cantidad * precio

        # -------------------------------------------------
        # ESTADO
        # -------------------------------------------------

        estado = request.form.get(
            "estado",
            factura.get("estado", "Pendiente")
        )

        # -------------------------------------------------
        # ACTUALIZAR FACTURA
        # -------------------------------------------------

        factura["cliente"] = cliente
        factura["producto"] = producto
        factura["cantidad"] = cantidad
        factura["total"] = total
        factura["estado"] = estado

        return redirect("/facturacion")

    return render_template(
        "editar_factura.html",
        factura=factura
    )


# ---------------------------------------------------------
# ELIMINAR FACTURA
# ---------------------------------------------------------

@app.route("/eliminar_factura/<int:id>")
def eliminar_factura(id):

    factura = next(
        (f for f in facturas_lista if f["id"] == id),
        None
    )

    if factura:
        facturas_lista.remove(factura)

    return redirect("/facturacion")


# =========================================================
# EJECUTAR APLICACIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)