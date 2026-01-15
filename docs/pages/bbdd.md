# Documentación inicial — Estructura de Base de Datos (Tablas)

## Gestor de Finanzas Personales (Web + App Móvil)

> Objetivo: definir un esquema relacional **claro, normalizado y escalable** para usuarios, movimientos (ingresos/gastos), categorías, tags y facturas/documentos.

---

## 1. Decisiones de diseño

### 1.1 Modelo de datos

- **Relacional** (tablas) para asegurar integridad, relaciones y consultas fáciles (resúmenes, filtros, estadísticas).
- Cada dato “propietario” pertenece a un **usuario** (multiusuario real).

### 1.2 Convenciones

- `id`: clave primaria (UUID o BIGINT autoincremental).
- `created_at`, `updated_at`: timestamps.
- Importes en **centavos** (enteros) para evitar errores de decimales.
  - Ej: 10,99 € → `1099` en `amount_cents`.
- Fechas:
  - `occurred_at`: fecha real del movimiento (cuando pasó).
  - `created_at`: cuando se guardó en la app.

### 1.3 Tipos recomendados

- `currency`: ISO 4217 (ej. `EUR`, `USD`).
- `type`: `income` | `expense`.
- `status`: opcional (`active`, `deleted`, etc.) si quieres “borrado lógico”.

---

## 2. Diagrama mental de relaciones (simple)

- Un **usuario** tiene muchas **categorías**
- Un **usuario** tiene muchos **movimientos**
- Un **movimiento** puede tener **1 categoría**
- Un **movimiento** puede tener **muchos tags** (N:M)
- Un **movimiento** puede tener **0..N adjuntos** (facturas/fotos)

---

## 3. Tablas principales

## 3.1 `users`

Usuarios del sistema.

**Campos**

- `id` (PK)
- `email` (UNIQUE)
- `password_hash`
- `display_name` (opcional)
- `default_currency` (ej. `EUR`)
- `created_at`
- `updated_at`

**Restricciones**

- `email` único
- `password_hash` obligatorio

**Índices recomendados**

- `UNIQUE(email)`

---

## 3.2 `categories`

Categorías de movimientos (Comida, Transporte…).

**Campos**

- `id` (PK)
- `user_id` (FK → users.id)
- `name` (texto)
- `color` (opcional: hex `#RRGGBB`)
- `icon` (opcional: nombre de icono)
- `created_at`
- `updated_at`

**Restricciones**

- Una categoría pertenece a un usuario.
- Nombre de categoría **único por usuario** (evita duplicados tipo “Comida” x2).

**Índices recomendados**

- `INDEX(user_id)`
- `UNIQUE(user_id, name)`

---

## 3.3 `tags`

Tags (etiquetas) flexibles (Trabajo, Viaje, Urgente…).

> Mejor que “tipo de gasto” fijo: permite múltiples etiquetas por movimiento.

**Campos**

- `id` (PK)
- `user_id` (FK → users.id)
- `name`
- `created_at`
- `updated_at`

**Restricciones**

- Tag único por usuario: `UNIQUE(user_id, name)`

**Índices recomendados**

- `INDEX(user_id)`
- `UNIQUE(user_id, name)`

---

## 3.4 `transactions` (movimientos)

Ingresos y gastos.

**Campos**

- `id` (PK)
- `user_id` (FK → users.id)
- `category_id` (FK → categories.id, NULL permitido)
- `type` (`income` | `expense`)
- `amount_cents` (entero)
- `currency` (ej. `EUR`)
- `title` (concepto corto: “Supermercado”)
- `notes` (opcional)
- `occurred_at` (fecha del movimiento)
- `created_at`
- `updated_at`

**Restricciones**

- `amount_cents > 0` (si quieres devoluciones, se controla con lógica de negocio)
- `type` solo valores permitidos
- `category_id` puede ser NULL (si el usuario no asigna)

**Índices recomendados**

- `INDEX(user_id, occurred_at)`
- `INDEX(user_id, type)`
- `INDEX(user_id, category_id)`
- (Opcional) `FULLTEXT(title, notes)` si tu BD lo soporta

---

## 3.5 `transaction_tags` (tabla intermedia N:M)

Relación muchos a muchos entre movimientos y tags.

**Campos**

- `transaction_id` (FK → transactions.id)
- `tag_id` (FK → tags.id)
- `created_at`

**Clave primaria**

- PK compuesta: `(transaction_id, tag_id)`  
  (evita duplicados)

**Índices recomendados**

- `INDEX(tag_id)`
- `INDEX(transaction_id)`

---

## 3.6 `attachments` (facturas / documentos)

Archivos asociados a un movimiento (foto, PDF, etc.).  
Almacenamiento en S3/MinIO: aquí guardas metadata y URL/clave.

**Campos**

- `id` (PK)
- `user_id` (FK → users.id)
- `transaction_id` (FK → transactions.id)
- `storage_provider` (ej. `minio`)
- `bucket` (ej. `receipts`)
- `object_key` (clave del objeto en S3/MinIO)
- `original_filename`
- `mime_type` (ej. `image/jpeg`, `application/pdf`)
- `size_bytes`
- `uploaded_at`
- `created_at`
- `updated_at`

**Restricciones**

- Un adjunto siempre pertenece a un usuario y a un movimiento.
- `object_key` obligatorio.

**Índices recomendados**

- `INDEX(user_id)`
- `INDEX(transaction_id)`
- `INDEX(user_id, uploaded_at)`

---

## 4. Tablas opcionales (si metes extras)

## 4.1 `budgets` (presupuestos)

Presupuesto mensual por categoría.

**Campos**

- `id` (PK)
- `user_id` (FK)
- `category_id` (FK)
- `month` (YYYY-MM o fecha primer día del mes)
- `amount_cents`
- `currency`
- `created_at`
- `updated_at`

**Restricciones**

- Presupuesto único por usuario+categoría+mes: `UNIQUE(user_id, category_id, month)`

---

## 4.2 `ocr_extractions` (si haces OCR)

Resultados del OCR de una factura.

**Campos**

- `id` (PK)
- `attachment_id` (FK)
- `status` (`pending` | `done` | `failed`)
- `extracted_total_cents` (opcional)
- `extracted_date` (opcional)
- `raw_text` (opcional)
- `created_at`
- `updated_at`

---

## 5. Reglas de integridad y seguridad (importante)

### 5.1 Multi-tenant (datos por usuario)

Todas las consultas deben filtrar por `user_id`.

- Ej: al pedir movimientos: `WHERE user_id = :currentUser`

### 5.2 Contraseñas

- Guardar solo `password_hash` (hash seguro tipo bcrypt/argon2).
- Nunca guardar contraseñas en texto plano.

### 5.3 Eliminación

Dos opciones:

1. **Borrado real** (DELETE) — más simple
2. **Borrado lógico** (campo `deleted_at`) — útil para recuperar/estadísticas  
   Elige una y sé consistente.

---

## 6. Consultas típicas que tu API necesitará (para validar el diseño)

### 6.1 Historial filtrado

- Por fecha: `user_id + occurred_at`
- Por categoría
- Por tipo (income/expense)
- Por tags (join con `transaction_tags`)

### 6.2 Resumen mensual

- Total ingresos mes
- Total gastos mes
- Balance = ingresos − gastos
- Top categorías por gasto

---

## 7. Checklist de implementación

- [ ] Crear migraciones de tablas
- [ ] Definir constraints (UNIQUE, FK, CHECK)
- [ ] Crear índices principales
- [ ] Semillas (seed) de categorías por defecto
- [ ] Probar queries de resumen con datos reales de ejemplo

---

## 8. Nota final (para tu memoria)

Este esquema está normalizado y cubre:

- CRUD de movimientos, categorías y tags
- Filtros por fecha/categoría/tipo
- Adjuntos con MinIO (S3 compatible)
- Resúmenes y estadísticas
- Base sólida para presupuestos y OCR (opcionales)
b