
# DB/models.py
# Funciones de acceso a datos para usuarios y equipos

def get_conn(db):
    """Obtiene la conexión desde el objeto OracleDB."""
    return db.connection


# ---------- LOGIN ----------
def validar_usuario(db, username, password):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """SELECT ID_USUARIO, USERNAME, ROL
               FROM USUARIO
               WHERE USERNAME = :u AND PASSWORD = :p""",
        u=username, p=password
    )
    row = cur.fetchone()
    cur.close()

    if row:
        return {
            "id_usuario": row[0],
            "username": row[1],
            "rol": row[2]
        }
    return None


# ---------- EQUIPOS: LISTAR ----------
def obtener_equipos(db):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """SELECT
                   e.ID_EQUIPO,
                   e.NOMBRE,
                   e.AFORO,
                   e.ANO_FUNDACION,
                   u.DEPARTAMENTO,
                   u.MUNICIPIO
               FROM EQUIPO e
               JOIN UBICACION u ON u.ID_UBICACION = e.ID_UBICACION
               ORDER BY e.NOMBRE"""
    )
    equipos = []
    for row in cur:
        equipos.append({
            "id_equipo":     row[0],
            "nombre":        row[1],
            "aforo":         row[2],
            "ano_fundacion": row[3],
            "departamento":  row[4],
            "municipio":     row[5],
        })
    cur.close()
    return equipos


# ---------- EQUIPOS: GET POR ID ----------
def obtener_equipo_por_id(db, id_equipo):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """SELECT
                   ID_EQUIPO,
                   NOMBRE,
                   AFORO,
                   ANO_FUNDACION,
                   ID_PRESIDENTE,
                   ID_UBICACION
               FROM EQUIPO
               WHERE ID_EQUIPO = :id""", id=id_equipo
    )
    row = cur.fetchone()
    cur.close()

    if not row:
        return None

    return {
        "id_equipo":     row[0],
        "nombre":        row[1],
        "aforo":         row[2],
        "ano_fundacion": row[3],
        "id_presidente": row[4],
        "id_ubicacion":  row[5],
    }


# ---------- EQUIPOS: INSERT ----------
def crear_equipo(db, nombre, aforo, ano_fundacion, id_presidente, id_ubicacion):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO EQUIPO
                   (NOMBRE, AFORO, ANO_FUNDACION, ID_PRESIDENTE, ID_UBICACION)
               VALUES (:nombre, :aforo, :ano_fundacion, :id_presidente, :id_ubicacion)""",
        nombre=nombre,
        aforo=aforo,
        ano_fundacion=ano_fundacion,
        id_presidente=id_presidente,
        id_ubicacion=id_ubicacion
    )
    conn.commit()
    cur.close()


# ---------- EQUIPOS: UPDATE ----------
def actualizar_equipo(db, id_equipo, nombre, aforo, ano_fundacion, id_presidente, id_ubicacion):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """UPDATE EQUIPO
               SET NOMBRE = :nombre,
                   AFORO = :aforo,
                   ANO_FUNDACION = :ano_fundacion,
                   ID_PRESIDENTE = :id_presidente,
                   ID_UBICACION = :id_ubicacion
               WHERE ID_EQUIPO = :id_equipo""",
        id_equipo=id_equipo,
        nombre=nombre,
        aforo=aforo,
        ano_fundacion=ano_fundacion,
        id_presidente=id_presidente,
        id_ubicacion=id_ubicacion
    )
    conn.commit()
    cur.close()


# ---------- EQUIPOS: DELETE ----------
def eliminar_equipo(db, id_equipo):
    conn = get_conn(db)
    cur = conn.cursor()
    cur.execute(
        """DELETE FROM EQUIPO
               WHERE ID_EQUIPO = :id_equipo""", id_equipo=id_equipo
    )
    conn.commit()
    cur.close()
