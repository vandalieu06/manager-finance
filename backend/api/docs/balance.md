# Balance

Consulta del balance financiero del usuario autenticado.

## Autenticación requerida

El endpoint de balance requiere autenticación JWT. Incluir el token en el header:

```
Authorization: Bearer <token>
```

---

## Obtener balance

Retorna el balance financiero total del usuario autenticado, incluyendo ingresos, gastos y el balance neto.

### Ruta y método HTTP

```
GET /api/balance
```

### Parámetros

**Query Parameters**

| Campo    | Tipo   | Requerido | Descripción                                         |
| -------- | ------ | --------- | --------------------------------------------------- |
| currency | string | No        | Código de moneda (3 caracteres). Por defecto: `EUR` |

### Ejemplo de request

```bash
# Balance en euros (por defecto)
curl -X GET http://localhost:8080/api/balance \
  -H "Authorization: Bearer <token>"

# Balance en dólares
curl -X GET "http://localhost:8080/api/balance?currency=USD" \
  -H "Authorization: Bearer <token>"
```

### Ejemplo de response

```json
{
  "total_income": 500000,
  "total_expense": 125000,
  "balance": 375000,
  "currency": "EUR"
}
```

### Códigos de respuesta

| Código | Descripción                              |
|--------|------------------------------------------|
| 200    | OK - Balance obtenido                   |
| 400    | Bad Request - Moneda no soportada       |
| 401    | Unauthorized - Token no proporcionado   |

### Notas técnicas

- **total_income**: Suma de todos los ingresos en centavos.
- **total_expense**: Suma de todos los gastos en centavos.
- **balance**: Diferencia entre ingresos y gastos (total_income - total_expense).
- Los montos se expresan en centavos (ej: 500000 = €5000.00).
- La moneda por defecto es EUR.
- El balance se calcula en tiempo real basándose en todas las transacciones del usuario.
- Si el usuario no tiene transacciones, el balance será 0.
