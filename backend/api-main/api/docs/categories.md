# Categorías

Gestión de categorías para clasificar transacciones financieras.

## Autenticación requerida

Todos los endpoints de categorías requieren autenticación JWT. Incluir el token en el header:

```
Authorization: Bearer <token>
```

---

## Crear categoría

Registra una nueva categoría para clasificar transacciones.

### Ruta y método HTTP

```
POST /api/categories
```

### Parámetros

**Body (JSON)**

| Campo    | Tipo   | Requerido | Descripción                              |
|----------|--------|-----------|------------------------------------------|
| name     | string | Sí        | Nombre de la categoría (1-100 caracteres)|
| type     | string | Sí        | Tipo: `income` o `expense`              |
| parent_id| uint   | No        | ID de la categoría padre (para subcategorías) |

### Ejemplo de request

```json
{
  "name": "Transporte",
  "type": "expense",
  "parent_id": null
}
```

```bash
curl -X POST http://localhost:8080/api/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Transporte",
    "type": "expense",
    "parent_id": null
  }'
```

### Ejemplo de response

```json
{
  "id": 5,
  "name": "Transporte",
  "type": "expense",
  "parent_id": null,
  "tags": [],
  "children": [],
  "created_at": "2026-03-16T10:00:00Z",
  "updated_at": "2026-03-16T10:00:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 201    | Created - Categoría creada exitosamente |
| 400    | Bad Request - Datos inválidos           |
| 401    | Unauthorized - Token no proporcionado   |

### Notas técnicas

- Las categorías pueden ser de tipo `income` (ingreso) o `expense` (gasto).
- Se pueden crear subcategorías indicando un `parent_id` válido.
- El nombre debe ser único dentro del mismo tipo y nivel.

---

## Obtener todas las categorías

Retorna todas las categorías disponibles, opcionalmente filtradas por tipo.

### Ruta y método HTTP

```
GET /api/categories
```

### Parámetros

**Query Parameters**

| Campo | Tipo   | Requerido | Descripción                    |
|-------|--------|-----------|--------------------------------|
| type  | string | No        | Filtrar por tipo: `income` o `expense` |

### Ejemplo de request

```bash
# Todas las categorías
curl -X GET http://localhost:8080/api/categories \
  -H "Authorization: Bearer <token>"

# Solo categorías de gasto
curl -X GET "http://localhost:8080/api/categories?type=expense" \
  -H "Authorization: Bearer <token>"
```

### Ejemplo de response

```json
[
  {
    "id": 1,
    "name": "Salario",
    "type": "income",
    "parent_id": null,
    "tags": [],
    "children": [
      {
        "id": 2,
        "name": "Salario mensual",
        "type": "income",
        "parent_id": 1,
        "tags": [],
        "children": [],
        "created_at": "2026-01-10T08:00:00Z",
        "updated_at": "2026-01-10T08:00:00Z"
      }
    ],
    "created_at": "2026-01-10T08:00:00Z",
    "updated_at": "2026-01-10T08:00:00Z"
  },
  {
    "id": 3,
    "name": "Alimentación",
    "type": "expense",
    "parent_id": null,
    "tags": [],
    "children": [],
    "created_at": "2026-01-10T08:00:00Z",
    "updated_at": "2026-01-10T08:00:00Z"
  }
]
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Categorías obtenidas               |
| 401    | Unauthorized - Token no proporcionado   |

### Notas técnicas

- Las categorías incluyen sus subcategorías en el campo `children`.
- Si se proporciona el parámetro `type`, filtra por ese tipo.

---

## Obtener categoría por ID

Retorna una categoría específica por su identificador.

### Ruta y método HTTP

```
GET /api/categories/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción          |
|-------|--------|----------------------|
| id    | uint   | ID de la categoría   |

### Ejemplo de request

```bash
curl -X GET http://localhost:8080/api/categories/3 \
  -H "Authorization: Bearer <token>"
```

### Ejemplo de response

```json
{
  "id": 3,
  "name": "Alimentación",
  "type": "expense",
  "parent_id": null,
  "tags": [
    {
      "id": 5,
      "name": "Comida",
      "user_id": 1
    }
  ],
  "children": [],
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-01-10T08:00:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Categoría encontrada                |
| 400    | Bad Request - ID inválido               |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Categoría no encontrada     |

### Notas técnicas

- La respuesta incluye las etiquetas asociadas en `tags`.
- Las subcategorías se incluyen en `children`.

---

## Actualizar categoría

Modifica una categoría existente.

### Ruta y método HTTP

```
PUT /api/categories/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción          |
|-------|--------|----------------------|
| id    | uint   | ID de la categoría   |

**Body (JSON)**

| Campo    | Tipo   | Requerido | Descripción                              |
|----------|--------|-----------|------------------------------------------|
| name     | string | No        | Nombre de la categoría (1-100 caracteres)|
| type     | string | No        | Tipo: `income` o `expense`              |
| parent_id| uint   | No        | ID de la categoría padre                 |

### Ejemplo de request

```json
{
  "name": "Alimentación y supermercado"
}
```

```bash
curl -X PUT http://localhost:8080/api/categories/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Alimentación y supermercado"
  }'
```

### Ejemplo de response

```json
{
  "id": 3,
  "name": "Alimentación y supermercado",
  "type": "expense",
  "parent_id": null,
  "tags": [],
  "children": [],
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-03-16T12:00:00Z"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Categoría actualizada               |
| 400    | Bad Request - Datos inválidos           |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Categoría no encontrada     |

### Notas técnicas

- Solo se actualizan los campos proporcionados.
- Los campos omitidos mantienen su valor anterior.

---

## Eliminar categoría

Elimina una categoría existente.

### Ruta y método HTTP

```
DELETE /api/categories/{id}
```

### Parámetros

**Path Parameters**

| Campo | Tipo   | Descripción          |
|-------|--------|----------------------|
| id    | uint   | ID de la categoría   |

### Ejemplo de request

```bash
curl -X DELETE http://localhost:8080/api/categories/3 \
  -H "Authorization: Bearer <token>"
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 204    | No Content - Categoría eliminada        |
| 400    | Bad Request - ID inválido o categoría en uso |
| 401    | Unauthorized - Token no proporcionado   |
| 404    | Not Found - Categoría no encontrada     |

### Notas técnicas

- La eliminación es permanente.
- Si la categoría tiene transacciones asociadas, no se puede eliminar y retornará 400.
- Las subcategorías también se eliminan en cascada.
