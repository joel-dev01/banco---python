from flask import Flask, request, jsonify
from banco import Banco
from cuenta import Cuenta
from politicas import ComisionFija, Cashback
from db import obtener_cuentas, obtener_cuenta_por_id, eliminar_cuenta_db, transferir, obtener_movimientos, actualizar_saldo_db, crear_db, crear_tabla_movimientos


app = Flask(__name__)
banco = Banco()

@app.route("/")
def inicio():
    return "API funcionando"


@app.route("/cuentas", methods=["POST"])
def crear_cuenta():
    data = request.json

    titular = data.get("titular")
    saldo = data.get("saldo", 0)

    cuenta = Cuenta(
        titular,
        saldo,
        politicas=[ComisionFija(), Cashback()]
    )

    banco.agregar_cuenta(cuenta)

    return jsonify({
        "mensaje": "Cuenta creada",
        "id": cuenta.id
    }), 201



    
@app.route("/cuentas", methods=["GET"])
def listar_cuentas():
    

    cuentas = obtener_cuentas()

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
def obtener_cuenta(id):

    fila = obtener_cuenta_por_id(id)

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
def eliminar_cuenta(id):

    eliminado = eliminar_cuenta_db(id)

    if not eliminado:
        return jsonify({
            "error": "Cuenta no encontrada"
        }), 404

    return "", 204
    

@app.route("/transferencias", methods=["POST"])
def crear_transferencia():

    data = request.json
    if not data:
        return jsonify({
            "error": "JSON invalido"
        }), 400

    origen_id = data.get("origen_id")
    destino_id = data.get("destino_id")
    monto = data.get("monto")

    if origen_id is None or destino_id is None or monto is None:
        return jsonify({"error": "Datos incompletos"}), 400

    exito, mensaje = transferir(origen_id, destino_id, monto)

    if not exito:
        return jsonify({"error": mensaje}), 400

    return jsonify({"mensaje": mensaje}), 200
@app.route("/cuentas/<id>/movimientos", methods=["GET"])
def ver_movimientos(id):

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

    actualizado = actualizar_saldo_db(id, nuevo_saldo)

    if actualizado == 0:
        return jsonify({
            "error": "Cuenta no encontrada"
        }), 404

    return jsonify({
        "mensaje": "Saldo actualizado"
    }), 200

if __name__ == "__main__":
    crear_db()
    crear_tabla_movimientos()
    app.run(debug=True)
    



