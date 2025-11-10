
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

from DB.oracle_db import OracleDB
from DB import models

app = Flask(__name__)

# Clave para sesiones (cámbiala en producción)
app.secret_key = "cambia_esta_clave_secreta"

# Configuración de conexión a Oracle
# AJUSTA estos valores según tu instalación
db = OracleDB(
    user="liga_user",
    password="liga123",
    dsn="localhost:1521/XEPDB1",
)


# --------- DECORADORES DE SEGURIDAD ---------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if session.get("role") != role:
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("listar_equipos"))
            return f(*args, **kwargs)
        return wrapper
    return decorator


# --------- RUTAS ---------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("listar_equipos"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        usuario = models.validar_usuario(db, username, password)
        if usuario:
            session["user_id"] = usuario["id_usuario"]
            session["username"] = usuario["username"]
            session["role"] = usuario["rol"]
            flash(f"Bienvenido, {usuario['username']}", "success")
            return redirect(url_for("listar_equipos"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# --------- VISTA PARA AMBOS ROLES (solo consulta para básico) ---------
@app.route("/equipos")
def listar_equipos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    equipos = models.obtener_equipos(db)
    es_admin = session.get("role") == "admin"
    return render_template("equipo.html", equipo=equipos, es_admin=es_admin)


# --------- CRUD SOLO ADMIN ---------
@app.route("/equipos/nuevo", methods=["GET", "POST"])
def crear_equipo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for("listar_equipos"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        aforo = request.form.get("aforo") or None
        ano_fundacion = request.form.get("ano_fundacion") or None
        id_presidente = request.form.get("id_presidente")
        id_ubicacion = request.form.get("id_ubicacion")

        models.crear_equipo(
            db, nombre, aforo, ano_fundacion, id_presidente, id_ubicacion
        )
        flash("Equipo creado correctamente.", "success")
        return redirect(url_for("listar_equipos"))

    return render_template("equipo_form.html", action="Crear", equipo=None)


@app.route("/equipos/<int:id_equipo>/editar", methods=["GET", "POST"])
def editar_equipo(id_equipo):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for("listar_equipos"))

    equipo = models.obtener_equipo_por_id(db, id_equipo)
    if not equipo:
        flash("Equipo no encontrado.", "warning")
        return redirect(url_for("listar_equipos"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        aforo = request.form.get("aforo") or None
        ano_fundacion = request.form.get("ano_fundacion") or None
        id_presidente = request.form.get("id_presidente")
        id_ubicacion = request.form.get("id_ubicacion")

        models.actualizar_equipo(
            db, id_equipo, nombre, aforo, ano_fundacion, id_presidente, id_ubicacion
        )
        flash("Equipo actualizado correctamente.", "success")
        return redirect(url_for("listar_equipos"))

    return render_template("equipo_form.html", action="Editar", equipo=equipo)


@app.route("/equipos/<int:id_equipo>/eliminar", methods=["POST"])
def eliminar_equipo(id_equipo):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("No tienes permisos para acceder a esta página.", "danger")
        return redirect(url_for("listar_equipos"))

    models.eliminar_equipo(db, id_equipo)
    flash("Equipo eliminado correctamente.", "info")
    return redirect(url_for("listar_equipos"))


if __name__ == "__main__":
    app.run(debug=True)
