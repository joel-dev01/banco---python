# API Banco - Flask

API REST desarrollada con Flask y SQLite para gestionar cuentas bancarias.

## Funcionalidades

- Crear cuentas
- Listar cuentas
- Obtener cuenta por ID
- Actualizar saldo
- Eliminar cuentas
- Transferencias entre cuentas
- Historial de movimientos
- Filtros de movimientos

## Tecnologías

- Python
- Flask
- SQLite
- Postman

## Endpoints

### Crear cuenta
POST /cuentas

### Listar cuentas
GET /cuentas

### Obtener cuenta
GET /cuentas/<id>

### Actualizar saldo
PUT /cuentas/<id>

### Eliminar cuenta
DELETE /cuentas/<id>

### Transferencias
POST /transferencias

### Movimientos
GET /cuentas/<id>/movimientos
