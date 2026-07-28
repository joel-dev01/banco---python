import sqlite3
from datetime import datetime


def get_connection():
    conexion = sqlite3.connect("banco.db")
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion



def crear_db():
    conexion = get_connection()
    cursor = conexion.cursor()
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cuentas (
        id TEXT PRIMARY KEY,
        titular TEXT,
        saldo REAL,
        usuario_id INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE

    )""")
    conexion.commit()
    conexion.close()

def insertar_usuario(email, password_hash):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO usuarios (email, password_hash)
    VALUES (?, ?)
    """, (email, password_hash))

    conexion.commit()
    usuario_id = cursor.lastrowid
    conexion.close()
    return usuario_id

def obtener_usuario_por_email(email):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, email, password_hash
    FROM usuarios
    WHERE email = ?
    """, (email,))

    fila = cursor.fetchone()
    conexion.close()
    return fila

def crear_tabla_movimientos():
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cuenta_id TEXT,
        tipo TEXT,
        monto REAL,
        fecha TEXT,
        FOREIGN KEY (cuenta_id) REFERENCES cuentas(id)
        ON DELETE CASCADE
    )
    """)

    conexion.commit()
    conexion.close()

    
def insertar_cuenta(cuenta,user_id):
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO cuentas (id, titular, saldo, usuario_id)
    VALUES (?, ?, ?, ?)
    """, (cuenta.id, cuenta.titular, cuenta.saldo, user_id))

    conexion.commit()
    conexion.close()
      
    
def obtener_cuentas(usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, titular, saldo FROM cuentas WHERE usuario_id = ?",
        (usuario_id,)
    )
    filas = cursor.fetchall()
    
    conexion.close()
    return filas

    


def obtener_cuenta_por_id(cuenta_id, usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, titular, saldo
        FROM cuentas
        WHERE id = ? AND usuario_id = ?
    """, (cuenta_id, usuario_id))

    fila = cursor.fetchone()
    conexion.close()
    return fila


def actualizar_saldo_db(cuenta_id, nuevo_saldo, usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE cuentas 
        SET saldo = ?
        WHERE id = ? AND usuario_id = ?
        """,
        (nuevo_saldo, cuenta_id, usuario_id) )
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas


def eliminar_cuenta_db(cuenta_id, usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM cuentas WHERE id = ? AND usuario_id = ?", (cuenta_id, usuario_id))

        if cursor.rowcount == 0:
            conexion.rollback()
            return False

        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        return False

    finally:
        conexion.close()

    
def insertar_movimiento(cuenta_id, tipo, monto, fecha):
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    INSERT INTO movimientos (cuenta_id, tipo, monto, fecha)
    VALUES (?, ?, ?, ?)
    """, (cuenta_id, tipo, monto, fecha))

    conexion.commit()
    conexion.close()
    

def obtener_movimientos(cuenta_id):
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT tipo, monto, fecha
    FROM movimientos
    WHERE cuenta_id = ?
    ORDER BY fecha DESC
    """, (cuenta_id,))

    filas = cursor.fetchall()
    conexion.close()
    return filas

        
def obtener_movimientos_filtrados(cuenta_id, tipo):
        
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT tipo, monto, fecha
    FROM movimientos
    WHERE cuenta_id = ? AND tipo = ?
    ORDER BY fecha DESC
    """, (cuenta_id, tipo))

    filas = cursor.fetchall()
    conexion.close()
    return filas


def buscar_movimientos(
    cuenta_id,
    tipo=None,
    fecha_desde=None,
    fecha_hasta=None,
    monto_min=None,
    monto_max=None
):
    
    conexion = get_connection()
    cursor = conexion.cursor()

    query = """
    SELECT tipo, monto, fecha
    FROM movimientos
    WHERE cuenta_id = ?
    """
    params = [cuenta_id]

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    if fecha_desde:
        query += " AND fecha >= ?"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND fecha <= ?"
        params.append(fecha_hasta)

    if monto_min is not None:
        query += " AND monto >= ?"
        params.append(monto_min)

    if monto_max is not None:
        query += " AND monto <= ?"
        params.append(monto_max)

    query += " ORDER BY fecha DESC"

    cursor.execute(query, params)
    filas = cursor.fetchall()
    conexion.close()
    return filas


def transferir(origen_id, destino_id, monto, usuario_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if origen_id == destino_id:
            return False, "No podes transferirte a vos mismo"

        # Obtener saldo origen y verificar propiedad
        cursor.execute("SELECT saldo FROM cuentas WHERE id = ? AND usuario_id = ?", (origen_id, usuario_id))
        fila_origen = cursor.fetchone()

        if not fila_origen:
            return False, "Cuenta origen no existe o no pertenece al usuario"

        saldo_origen = fila_origen[0]
        if monto <= 0:
            return False, "Monto invalido"

        if saldo_origen < monto:
            return False, "Saldo insuficiente"

        # Verificar destino (no es necesario que pertenezca al mismo usuario)
        cursor.execute("SELECT saldo FROM cuentas WHERE id = ?", (destino_id,))
        fila_destino = cursor.fetchone()

        if not fila_destino:
            return False, "Cuenta destino no existe"

        # Restar saldo origen
        cursor.execute(
            "UPDATE cuentas SET saldo = saldo - ? WHERE id = ?",
            (monto, origen_id)
        )

        # Sumar saldo destino
        cursor.execute(
            "UPDATE cuentas SET saldo = saldo + ? WHERE id = ?",
            (monto, destino_id)
        )

        # Registrar movimientos
        cursor.execute(
            "INSERT INTO movimientos (cuenta_id, tipo, monto, fecha) VALUES (?, ?, ?, ?)",
            (origen_id, "transferencia_salida", monto, fecha)
        )

        cursor.execute(
            "INSERT INTO movimientos (cuenta_id, tipo, monto, fecha) VALUES (?, ?, ?, ?)",
            (destino_id, "transferencia_entrada", monto, fecha)
        )

        conexion.commit()
        return True, "Transferencia exitosa"

    except Exception:
        conexion.rollback()
        return False, "Error interno"

    finally:
        conexion.close()
        