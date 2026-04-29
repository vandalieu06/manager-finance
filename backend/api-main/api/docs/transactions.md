# Transacciones

Gestión de transacciones financieras (ingresos y gastos).

## Autenticación requerida

Todos los endpoints de transacciones requieren autenticación JWT. Incluir el token en el header:

```
Authorization: Bearer <token>
```

---

## Crear transacción

Registra una nueva transacción financiera.

### Ruta y método HTTP

```
POST /api/transactions
```

### Parámetros

**Body (JSON)**

| Campo      | Tipo    | Requerido | Descripción                              |
|------------|---------|-----------|------------------------------------------|
| type       | string  | Sí        | Tipo: `income` o `expense`               |
| amount     | int64   | Sí        | Monto en centavos (ej: 1000 = €10.00)   |
| currency   | string  | Sí        | Código de moneda (3 caracteres, ej: EUR)|
| description| string  | No        | Descripción de la transacción            |
| move_date  | string  | Sí        | Fecha de la transacción (ISO 8601)      |
| category_id| uint    | Sí        | ID de la categoría                       |
| code       | string  | No        | Código identificador único              |
| tag_ids    | []uint  | No        | IDs de etiquetas asociadas              |

### Ejemplo de request

```json
{
  "type": "expense",
  "amount": 2500,
  "currency": "EUR",
  "description": "Compra semanal de supermercado",
  "move_date": "2026-03-15T10:30:00Z",
  "category_id": 3,
  "code": "EXP-001",
  "tag_ids": [1, 5]
}
```

```bash
curl -X POST http://localhost:8080/api/transactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "type": "expense",
    "amount": 2500,
    "currency": "EUR",
    "description": "Compra semanal de supermercado",
    "move_date": "2026-03-15T10:30:00Z",
    "category_id": 3,
    "code": "EXP-001",
    "tag_ids": [1, 5]
  }'
```

### Ejemplo de response

```json
{
  "id": 42,
  "code": "EXP-001",
  "type": "expense",
  "amount": 2500,
  "currency": "EUR",
  "description": "Compra semanal de supermercado",
  "move_date": "2026-03-15T10:30:00Z",
  "category_id": 3,
  "category": {
    "id": 3,
    "name": "Supermercado",
    "type": "expense",
    "parent_id": null,
    "tags": [],
    "children": [],
    "created_at": "2026-01-10T08:00:00Z",
    "updated_at": "2026-01-10T08:00:00Z"
  },
  "user_id": 1,
  "tags": [
    {"id": 1, "name": "Semanal", "user_id": 1},
    {"id": 5, "name": "Alimentación", "user_id": 1}
  ],
  "created_at": "2026-03-16T09:15:00Z",
  "updated_at": "2026-03-16T09:15:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 201    | Created - Transacción creada exitosamente|
| 400    | Bad Request - Datos inválidos           |
| 401    | Unauthorized - Token no proporcionado   |

### Notas técnicas

- El monto se almacena en centavos para evitar problemas de precisión con decimales.
- El campo `code` es opcional pero debe ser único si se proporciona.
- La categoría debe existir y puede ser de tipo `income` o `expense`.

---

## Obtener todas las transacciones

Retorna todas las transacciones del usuario autenticado.

### Ruta y método HTTP

```
GET /api/transactions
```

### Parámetros

No requiere parámetros. Retorna todas las transacciones del usuario.

### Ejemplo de request

```bash
curl -X GET http://localhost:8080/api/transactions \
  -H "Authorization: Bearer <token>"
```

### Ejemplo de response

```json
[
  {
    "id": 42,
    "code": "EXP-001",
    "type": "expense",
    "amount": 2500,
    "currency": "EUR",
    "description": "Compra semanal de supermercado",
    "move_date": "2026-03-15T10:30:00Z",
    "category_id": 3,
    "category": {
      "id": 3,
      "name": "Supermercado",
      "type": "expense"
    },
    "user_id": 1,
    "tags": [],
    "created_at": "2026-03-16T09:15:00Z",
    "updated_at": "2026-03-16T09:15:00Z"
  },
  {
    "id": 41,
    "code": "INC-001",
    "type": "income",
    "amount": 150000,
    "currency": "EUR",
    "description": "Salario mensual",
    "move_date": "2026-03-01T00:00:00Z",
    "category_id": 1,
    "category": {
      "id": 1,
      "name": "Salario",
      "type": "income"
    },
    "user_id": 1,
    "tags": [],
    "created_at": "2026-03-02T08:00:00Z",
    "updated_at": "2026-03-02T08:00:00Z"
  }
]
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Transacciones obtenidas            |
| 401    | Unauthorized - Token no proporcionado   |

### Notas técnicas

- Las transacciones se retornan en orden descendente por fecha de creación.
- Solo se retornan las transacciones del usuario autenticado.

---

## Obtener transacción por ID

Retorna una transacción específica por su identificador.

### Ruta y método HTTP

```
GET /api/transactions/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción              |
|-------|--------|--------------------------|
| id    | uint   | ID de la transacción     |

### Ejemplo de request

```bash
curl -X GET http://localhost:8080/api/transactions/42 \
  -H "Authorization: Bearer <token>"
```

### Ejemplo de response

```json
{
  "id": 42,
  "code": "EXP-001",
  "type": "expense",
  "amount": 2500,
  "currency": "EUR",
  "description": "Compra semanal de supermercado",
  "move_date": "2026-03-15T10:30:00Z",
  "category_id": 3,
  "category": {
    "id": 3,
    "name": "Supermercado",
    "type": "expense"
  },
  "user_id": 1,
  "tags": [
    {"id": 1, "name": "Semanal", "user_id": 1}
  ],
  "created_at": "2026-03-16T09:15:00Z",
  "updated_at": "2026-03-16T09:15:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Transacción encontrada             |
| 400    | Bad Request - ID inválido               |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Transacción no encontrada   |

### Notas técnicas

- La transacción debe pertenecer al usuario autenticado.

---

## Actualizar transacción

Modifica una transacción existente.

### Ruta y método HTTP

```
PUT /api/transactions/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción              |
|-------|--------|--------------------------|
| id    | uint   | ID de la transacción     |

**Body (JSON)**

| Campo      | Tipo    | Requerido | Descripción                              |
|------------|---------|-----------|------------------------------------------|
| type       | string  | No        | Tipo: `income` o `expense`               |
| amount     | int64   | No        | Monto en centavos                        |
| currency   | string  | No        | Código de moneda (3 caracteres)         |
| description| string  | No        | Descripción de la transacción            |
| move_date  | string  | No        | Fecha de la transacción (ISO 8601)      |
| category_id| uint    | No        | ID de la categoría                       |
| code       | string  | No        | Código identificador único               |
| tag_ids    | []uint  | No        | IDs de etiquetas asociadas              |

### Ejemplo de request

```json
{
  "amount": 3000,
  "description": "Compra semanal de supermercado - actualizada"
}
```

```bash
curl -X PUT http://localhost:8080/api/transactions/42 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "amount": 3000,
    "description": "Compra semanal de supermercado - actualizada"
  }'
```

### Ejemplo de response

```json
{
  "id": 42,
  "code": "EXP-001",
  "type": "expense",
  "amount": 3000,
  "currency": "EUR",
  "description": "Compra semanal de supermercado - actualizada",
  "move_date": "2026-03-15T10:30:00Z",
  "category_id": 3,
  "category": {
    "id": 3,
    "name": "Supermercado",
    "type": "expense"
  },
  "user_id": 1,
  "tags": [],
  "created_at": "2026-03-16T09:15:00Z",
  "updated_at": "2026-03-16T12:00:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Transacción actualizada             |
| 400    | Bad Request - Datos inválidos           |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Transacción no encontrada   |

### Notas técnicas

- Solo se actualizan los campos proporcionados.
- Los campos omitidos mantienen su valor anterior.
- La transacción debe pertenecer al usuario autenticado.

---

## Eliminar transacción

Elimina una transacción existente.

### Ruta y método HTTP

```
DELETE /api/transactions/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción              |
|-------|--------|--------------------------|
| id    | uint   | ID de la transacción     |

### Ejemplo de request

```bash
curl -X DELETE http://localhost:8080/api/transactions/42 \
  -H "Authorization: Bearer <token>"
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 204    | No Content - Transacción eliminada      |
| 400    | Bad Request - ID inválido               |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Transacción no encontrada   |

### Notas técnicas

- La eliminación es permanente.
- La transacción debe pertenecer al usuario autenticado.
