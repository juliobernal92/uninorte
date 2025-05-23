# Uninorte
Proyecto de Programación V

## Pasos para probar el proyecto

### Instalar las librerías
```bash
pip install -r requirements.txt
```

### Crear la base de datos en PostgreSQL
Setear las credenciales.

### Prueba en Postman:

#### Registro:
```http
POST http://127.0.0.1:8000/api/auth/register/
```
```json
{
  "username": "usuario",
  "password": "contrasenha",
  "email": "usuario@example.com"
}
```

#### Login:
```http
POST http://127.0.0.1:8000/api/auth/login/
```
```json
{
  "username": "usuario",
  "password": "contrasenha"
}
```

Ahi se genera el JWT, que luego debe usarse para las demás aplicaciones.

### Autores:

#### Obtener Todos:
```http
GET http://127.0.0.1:8000/api/autores/
```
**Auth Type**: Bearer Token: el JWT generado.

#### Insertar:
```http
POST http://127.0.0.1:8000/api/autores/
```
```json
{
  "nombre": "Robert Louis Stevenson",
  "nacionalidad": "Escocés"
}
```
**Auth Type**: Bearer Token: el JWT generado.