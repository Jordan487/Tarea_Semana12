from flask import Flask, render_template, redirect, url_for
import sqlite3

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# ==================================================
# CONFIGURACIÓN DE FLASK
# ==================================================

app.config["SECRET_KEY"] = "mi_clave_secreta_2026"


# ==================================================
# CONFIGURACIÓN DE SQLITE
# ==================================================

DATABASE = "data/ferreteria.db"


def conectar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==================================================
# INICIALIZAR BASE DE DATOS
# ==================================================

def inicializar_bd():

    conn = conectar_bd()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# CARGAR PRODUCTOS INICIALES
# ==================================================

def cargar_productos_iniciales():

    conn = conectar_bd()

    cantidad = conn.execute(
        "SELECT COUNT(*) AS total FROM productos"
    ).fetchone()["total"]

    if cantidad == 0:

        productos_iniciales = [
            (
                "Registro Académico",
                "Administración de estudiantes",
                25.00
            ),
            (
                "Consulta Estudiantil",
                "Consulta de información académica",
                15.00
            ),
            (
                "Seguimiento Académico",
                "Seguimiento del desempeño estudiantil",
                20.00
            ),
            (
                "Certificado Académico",
                "Emisión de certificados para estudiantes",
                10.00
            )
        ]

        conn.executemany("""
            INSERT INTO productos
            (nombre, descripcion, precio)
            VALUES (?, ?, ?)
        """, productos_iniciales)

        conn.commit()

    conn.close()


# ==================================================
# FUNCIONES PARA PRODUCTOS
# ==================================================

def obtener_productos():

    conn = conectar_bd()

    productos = conn.execute("""
        SELECT id, nombre, descripcion, precio
        FROM productos
        ORDER BY id
    """).fetchall()

    conn.close()

    return productos


def obtener_producto_por_id(producto_id):

    conn = conectar_bd()

    producto = conn.execute("""
        SELECT id, nombre, descripcion, precio
        FROM productos
        WHERE id = ?
    """, (producto_id,)).fetchone()

    conn.close()

    return producto


def buscar_producto_por_nombre(nombre):

    conn = conectar_bd()

    producto = conn.execute("""
        SELECT id, nombre, descripcion, precio
        FROM productos
        WHERE nombre = ?
    """, (nombre,)).fetchone()

    conn.close()

    return producto


# ==================================================
# PÁGINA PRINCIPAL
# ==================================================

@app.route("/")
def inicio():

    return render_template("index.html")


# ==================================================
# PRODUCTOS
# ==================================================

@app.route("/productos")
def productos():

    productos = obtener_productos()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==================================================
# AGREGAR PRODUCTO
# ==================================================

@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_bd()

        conn.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.descripcion.data,

            # Convertimos Decimal a float para SQLite
            float(form.precio.data)
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "agregar_producto.html",
        form=form
    )


# ==================================================
# EDITAR PRODUCTO
# ==================================================

@app.route("/editar_producto/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):

    producto = obtener_producto_por_id(producto_id)

    if producto is None:

        return redirect(url_for("productos"))

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_bd()

        conn.execute("""
            UPDATE productos
            SET nombre = ?,
                descripcion = ?,
                precio = ?
            WHERE id = ?
        """, (
            form.nombre.data,
            form.descripcion.data,

            # Convertimos Decimal a float para SQLite
            float(form.precio.data),

            producto_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("productos"))

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]

    return render_template(
        "editar_producto.html",
        form=form,
        producto=producto
    )


# ==================================================
# ELIMINAR PRODUCTO
# ==================================================

@app.route("/eliminar_producto/<int:producto_id>")
def eliminar_producto(producto_id):

    conn = conectar_bd()

    conn.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (producto_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("productos"))


# ==================================================
# CLIENTES
# ==================================================

clientes_lista = [
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "cedula": "0102030405",
        "telefono": "0999999999",
        "correo": "juan@gmail.com"
    },
    {
        "id": 2,
        "nombre": "María González",
        "cedula": "0102030406",
        "telefono": "0988888888",
        "correo": "maria@gmail.com"
    }
]


@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


@app.route("/agregar_cliente", methods=["GET", "POST"])
def agregar_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_id = len(clientes_lista) + 1

        clientes_lista.append({
            "id": nuevo_id,
            "nombre": form.nombre.data,
            "cedula": form.cedula.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data
        })

        return redirect(url_for("clientes"))

    return render_template(
        "agregar_cliente.html",
        form=form
    )


@app.route("/editar_cliente/<int:cliente_id>", methods=["GET", "POST"])
def editar_cliente(cliente_id):

    cliente = next(
        (c for c in clientes_lista if c["id"] == cliente_id),
        None
    )

    if cliente is None:

        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():

        cliente["nombre"] = form.nombre.data
        cliente["cedula"] = form.cedula.data
        cliente["telefono"] = form.telefono.data
        cliente["correo"] = form.correo.data

        return redirect(url_for("clientes"))

    if not form.is_submitted():

        form.nombre.data = cliente["nombre"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.correo.data = cliente["correo"]

    return render_template(
        "editar_cliente.html",
        form=form,
        cliente=cliente
    )


# ==================================================
# PROVEEDORES
# ==================================================

proveedores_lista = [
    {
        "id": 1,
        "empresa": "Distribuidora ABC",
        "contacto": "Carlos López",
        "telefono": "0991111111",
        "correo": "abc@gmail.com"
    },
    {
        "id": 2,
        "empresa": "Proveedor XYZ",
        "contacto": "Ana Martínez",
        "telefono": "0992222222",
        "correo": "xyz@gmail.com"
    }
]


@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


@app.route("/agregar_proveedor", methods=["GET", "POST"])
def agregar_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_id = len(proveedores_lista) + 1

        proveedores_lista.append({
            "id": nuevo_id,
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data
        })

        return redirect(url_for("proveedores"))

    return render_template(
        "agregar_proveedor.html",
        form=form
    )


@app.route("/editar_proveedor/<int:proveedor_id>", methods=["GET", "POST"])
def editar_proveedor(proveedor_id):

    proveedor = next(
        (p for p in proveedores_lista if p["id"] == proveedor_id),
        None
    )

    if proveedor is None:

        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor["empresa"] = form.empresa.data
        proveedor["contacto"] = form.contacto.data
        proveedor["telefono"] = form.telefono.data
        proveedor["correo"] = form.correo.data

        return redirect(url_for("proveedores"))

    if not form.is_submitted():

        form.empresa.data = proveedor["empresa"]
        form.contacto.data = proveedor["contacto"]
        form.telefono.data = proveedor["telefono"]
        form.correo.data = proveedor["correo"]

    return render_template(
        "editar_proveedor.html",
        form=form,
        proveedor=proveedor
    )


# ==================================================
# FACTURACIÓN
# ==================================================

facturas_lista = []


@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


@app.route("/agregar_factura", methods=["GET", "POST"])
def agregar_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        producto = buscar_producto_por_nombre(
            form.producto.data
        )

        if producto:

            cantidad = form.cantidad.data

            subtotal = float(producto["precio"]) * cantidad

            nueva_factura = {
                "id": len(facturas_lista) + 1,
                "cliente": form.cliente.data,
                "producto": producto["nombre"],
                "cantidad": cantidad,
                "precio": float(producto["precio"]),
                "subtotal": subtotal
            }

            facturas_lista.append(nueva_factura)

            return redirect(url_for("facturacion"))

    return render_template(
        "agregar_factura.html",
        form=form
    )


@app.route("/editar_factura/<int:factura_id>", methods=["GET", "POST"])
def editar_factura(factura_id):

    factura = next(
        (f for f in facturas_lista if f["id"] == factura_id),
        None
    )

    if factura is None:

        return redirect(url_for("facturacion"))

    form = FacturacionForm()

    if form.validate_on_submit():

        producto = buscar_producto_por_nombre(
            form.producto.data
        )

        if producto:

            factura["cliente"] = form.cliente.data
            factura["producto"] = producto["nombre"]
            factura["cantidad"] = form.cantidad.data
            factura["precio"] = float(producto["precio"])
            factura["subtotal"] = (
                float(producto["precio"])
                * form.cantidad.data
            )

            return redirect(url_for("facturacion"))

    if not form.is_submitted():

        form.cliente.data = factura["cliente"]
        form.producto.data = factura["producto"]
        form.cantidad.data = factura["cantidad"]

    return render_template(
        "editar_factura.html",
        form=form,
        factura=factura
    )


# ==================================================
# INICIALIZAR BASE DE DATOS
# ==================================================

inicializar_bd()
cargar_productos_iniciales()


# ==================================================
# EJECUTAR APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)