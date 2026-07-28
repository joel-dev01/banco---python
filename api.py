import os
import sqlite3
import jwt
from functools import wraps
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, g
from extensions import bcrypt
from banco import Banco
from cuenta import Cuenta
from politicas import ComisionFija, Cashback
from db import (
    obtener_cuentas,
    insertar_usuario,
    obtener_cuenta_por_id,
    eliminar_cuenta_db,
    transferir,
    obtener_movimientos,
    actualizar_saldo_db,
    crear_db,
    crear_tabla_movimientos,
    obtener_usuario_por_email
)
app = Flask(__name__)

# Cargar variables de entorno si está disponible python-dotenv (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Leer SECRET_KEY desde la variable de entorno en producción
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super_secret_key_cambiar_en_produccion")
banco = Banco()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token requerido o mal formato"}), 401

        try:
            token = auth_header.split(" ")[1]

            data = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            g.user_id = data["user_id"]

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def inicio():
    return "API funcionando"


@app.route("/cuentas", methods=["POST"])
@token_required
def crear_cuenta():
    data = request.json

    titular = data.get("titular")
    saldo = data.get("saldo", 0)

    cuenta = Cuenta(
        titular,
        saldo,
        politicas=[ComisionFija(), Cashback()]
    )

    banco.agregar_cuenta(cuenta, g.user_id)

    return jsonify({
        "mensaje": "Cuenta creada",
        "id": cuenta.id
    }), 201

    
@app.route("/cuentas", methods=["GET"])
@token_required
def listar_cuentas():
    cuentas = obtener_cuentas(g.user_id)
    resultado = []
    for id, titular, saldo in cuentas:
        cuenta_dict = {
            "id": id,
            "titular": titular,
            "saldo": saldo
        }
        resultado.append(cuenta_dict)

    return jsonify(resultado)
 
 
@app.route("/cuentas/<id>", methods=["GET"])
@token_required
def obtener_cuenta(id):

    fila = obtener_cuenta_por_id(id, g.user_id)

    if not fila:
        return jsonify({
            "error": "Cuenta no encontrada"
        }), 404

    cuenta = {
        "id": fila[0],
        "titular": fila[1],
        "saldo": fila[2]
    }

    return jsonify(cuenta)


@app.route("/cuentas/<id>", methods=["DELETE"])
@token_required
def eliminar_cuenta(id):
    eliminado = eliminar_cuenta_db(id, g.user_id)
    if not eliminado:
        return jsonify({
            "error": "Cuenta no encontrada"
        }), 404

    return "", 204
    

@app.route("/transferencias", methods=["POST"])
@token_required
def crear_transferencia():

    data = request.json
    if not data:
        return jsonify({"error": "JSON invalido"}), 400

    origen_id = data.get("origen_id")
    destino_id = data.get("destino_id")
    monto = data.get("monto")

    if origen_id is None or destino_id is None or monto is None:
        return jsonify({"error": "Datos incompletos"}), 400

    
    try:
        monto = float(monto)
    except (ValueError, TypeError):
        return jsonify({"error": "Monto inválido"}), 400

    exito, mensaje = transferir(origen_id, destino_id, monto, g.user_id)

    if not exito:
        return jsonify({"error": mensaje}), 400

    return jsonify({"mensaje": mensaje}), 200


@app.route("/cuentas/<id>/movimientos", methods=["GET"])
@token_required
def ver_movimientos(id):
    # Verificar que la cuenta pertenece al usuario
    cuenta = obtener_cuenta_por_id(id, g.user_id)
    if not cuenta:
        return jsonify({"error": "Cuenta no encontrada"}), 404

    movimientos = obtener_movimientos(id)
    resultado = []
    for tipo, monto, fecha in movimientos:
        resultado.append({
            "tipo": tipo,
            "monto": monto,
            "fecha": fecha
        })

    return jsonify(resultado)


@app.route("/cuentas/<id>", methods=["PUT"])
@token_required
def actualizar_cuenta(id):
    data = request.json
    if not data:
        return jsonify({
            "error": "JSON inválido"
        }), 400

    nuevo_saldo = data.get("saldo")

    if nuevo_saldo is None:
        return jsonify({
            "error": "Falta saldo"
        }), 400

    if nuevo_saldo < 0:
        return jsonify({
            "error": "Saldo inválido"
        }), 400

    actualizado = actualizar_saldo_db(id, nuevo_saldo, g.user_id)

    if actualizado == 0:
        return jsonify({
            "error": "Cuenta no encontrada"
        }), 404

    return jsonify({
        "mensaje": "Saldo actualizado"
    }), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password son requeridos"}), 400

    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

    # Hash de contraseña
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        insertar_usuario(email, password_hash)
        return jsonify({
            "message": "Usuario creado correctamente",
            "email": email
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El email ya está registrado"}), 409

    
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password son requeridos"}), 400

    usuario = obtener_usuario_por_email(email)

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    password_hash = usuario[2]

    
    if not bcrypt.check_password_hash(password_hash, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    user_id = usuario[0]

    token = jwt.encode(
        {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "token": token
    }), 200
    
    
if __name__ == "__main__":
    crear_db()
    crear_tabla_movimientos()
    app.run(debug=True)
    



