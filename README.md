# 🏦 API Banco – Flask

API REST desarrollada con **Flask y SQLite** que simula un sistema bancario con autenticación JWT, gestión de cuentas y transferencias seguras mediante transacciones atómicas.

---

## 🚀 Características

- ✅ Registro y login con **JWT**
- ✅ Autenticación protegida con middleware (`token_required`)
- ✅ Gestión de cuentas por usuario autenticado
- ✅ Transferencias con **transacciones SQL (commit / rollback)**
- ✅ Registro automático de movimientos
- ✅ Historial de movimientos por cuenta
- ✅ Validaciones robustas de negocio
- ✅ Relaciones con claves foráneas y `ON DELETE CASCADE`
- ✅ Aislamiento de datos por usuario

---

## 🧠 Conceptos Implementados

- RESTful API design
- JWT Authentication
- Password hashing con bcrypt
- Transacciones atómicas (ACID)
- Foreign Keys en SQLite
- Manejo de errores HTTP
- Validaciones backend
- Separación de capas (API / DB)

---

## 🛠 Tecnologías

- Python 3
- Flask
- SQLite
- PyJWT
- Bcrypt
- Postman (testing)

---

## 📦 Endpoints Principales

### 🔐 Autenticación
- `POST /register`
- `POST /login`

### 🏦 Cuentas
- `POST /cuentas`
- `GET /cuentas`
- `GET /cuentas/<id>`
- `PUT /cuentas/<id>`
- `DELETE /cuentas/<id>`

### 💸 Transferencias
- `POST /transferencias`

### 📜 Movimientos
- `GET /cuentas/<id>/movimientos`

---

## ▶️ Ejecutar Localmente

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python api.py
```

La API inicia en:

```
http://127.0.0.1:5000
```

---

## 🔒 Seguridad

- Contraseñas almacenadas con hash seguro (bcrypt)
- Autenticación basada en JWT con expiración
- Aislamiento de cuentas por usuario autenticado
- Foreign keys activadas en SQLite

---

## 📌 Nota

Proyecto desarrollado con fines educativos para demostrar conocimientos en backend y arquitectura REST.