# Autenticación

Endpoints para el registro e inicio de sesión de usuarios.

## Registro de usuario

Creación de una nueva cuenta de usuario en el sistema.

### Ruta y método HTTP

```
POST /api/auth/register
```

### Parámetros

**Body (JSON)**

| Campo    | Tipo   | Requerido | Descripción                         |
| -------- | ------ | --------- | ----------------------------------- |
| username | string | Sí        | Nombre de usuario (3-50 caracteres) |
| email    | string | Sí        | Correo electrónico válido           |
| password | string | Sí        | Contraseña (mínimo 6 caracteres)    |

### Ejemplo de request

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepass123"
}
```

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "securepass123"
  }'
```

### Ejemplo de response

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "avatar_url": null
  }
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 201    | Created - Usuario creado exitosamente   |
| 400    | Bad Request - Datos inválidos o email duplicado |

### Notas técnicas

- El password se almacena hasheado utilizando bcrypt.
- El token JWT generado tiene una validez de 24 horas.
- El campo `avatar_url` puede ser null si el usuario no ha configurado un avatar.

---

## Inicio de sesión

Autenticación de usuario existente para obtener un token de acceso.

### Ruta y método HTTP

```
POST /api/auth/login
```

### Parámetros

**Body (JSON)**

| Campo   | Tipo   | Requerido | Descripción          |
|---------|--------|-----------|----------------------|
| email   | string | Sí        | Correo electrónico   |
| password| string | Sí        | Contraseña           |

### Ejemplo de request

```json
{
  "email": "johndoe@example.com",
  "password": "securepass123"
}
```

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "johndoe@example.com",
    "password": "securepass123"
  }'
```

### Ejemplo de response

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "avatar_url": "https://example.com/avatars/user1.jpg"
  }
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Autenticación exitosa              |
| 400    | Bad Request - Datos inválidos           |
| 401    | Unauthorized - Credenciales incorrectas |

### Notas técnicas

- El token JWT debe ser incluido en el header `Authorization` para endpoints protegidos: `Authorization: Bearer <token>`
- El token expira después de 24 horas.
- Las credenciales incorrectas retornan 401 sin especificar si el email o la contraseña son incorrectas (seguridad).
