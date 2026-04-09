# SPEC - Categorías de Gasto (50/30/20)

## Descripción General
Sistema de categorías basado en la regla financiera 50/30/20:
- **50% Obligación** - Gastos necesarios
- **30% Ocio** - Wants + EyC
- **20% Ahorros** - Reservas

---

## Estructura de Categorías

### 1. OBLIGACIÓN (50%)
Gastos necesarios para vivir

| Subcategoría | Icono | Color Token |
|--------------|-------|-------------|
| Supermercado | 🛒 | `category_obligacion.v1` (#4F46E5) |
| Facturas | 💡 | `secondary.v1` (#F76132) |
| Transporte | 🚌 | `primary.v1` (#4ECDC4) |
| Salud | 💊 | `feedback.danger.v1` (#EF4444) |
| Hogar | 🏠 | `accent2.v1` (#FF6B6B) |

### 2. OCIO (30%)
Wants + Essentials & Care

| Subcategoría | Icono | Color Token |
|--------------|-------|-------------|
| Restaurantes | 🍽️ | `accent2.v1` (#FF6B6B) |
| Entretenimiento | 🎮 | `accent1.v1` (#FFE66D) |
| Cine | 🎬 | `primary.v1` (#4ECDC4) |
| Viajes | ✈️ | `category_ocio.v1` (#A855F7) |
| **EyC** | | |
| Higiene personal | 🧴 | `feedback.info.v1` (#0EA5E9) |
| Cuidado personal | 💅 | `feedback.warning.v1` (#F59E0B) |
| Bebidas | ☕ | `accent2.v1` (#FF6B6B) |
| Ropa | 👕 | `accent1.v1` (#FFE66D) |
| Snacks | 🍿 | `feedback.warning.v1` (#F59E0B) |

### 3. AHORROS (20%)
Seguimiento de reservas/inversiones

| Subcategoría | Icono | Color Token |
|--------------|-------|-------------|
| Ahorros | 💰 | `category_ahorro.v1` (#10B981) |
| Inversiones | 📈 | `category_ahorro.v1` (#10B981) |

> ⚠️ **Importante**: Los colores de categoría usan los nuevos tokens (`category_obligacion.v1`, `category_ocio.v1`, `category_ahorro.v1`) con variantes v2-v4 disponibles para estados hover/selected.

---

## Componentes Figma

### Category Badge
```
┌─────────────────────┐
│ 🛒 Supermercado     │
└─────────────────────┘
```
- Estados: default, selected, disabled
- Variantes: small (lista), medium (chips), large (header)

### Category Selector
- Dropdown con grupos (Obligación/Ocio/Ahorros)
- Búsqueda de categorías
- Multi-select para filtros

### Filter Chips
- Mostrar categorías activas
- Quick remove (x)
- "Limpiar todo" option

### Budget Progress Widget
```
┌────────────────────────────┐
│ PRESUPUESTO               │
│                           │
│ Obligación  ████████░░ 50%│
│ Ocio        ██████░░░░░ 30%│
│ Ahorros    █████░░░░░░ 20%│
└────────────────────────────┘
```
- Barras de progreso por categoría
- Color: verde (OK), amarillo (cerca límite), rojo (excedido)
- Click para ver detalle

---

## En pantallas

### Home (Dashboard)
- Budget Progress Widget (opcional, debajo de stats)
- Chart por categoría (obligación vs ocio vs ahorros)

### Escanear Facturas
- Category Selector en cada producto
- Auto-clasificación sugerida

### Productos
- Filter Chips por categoría
- Filtros por subcategoría

### Configuración
- CRUD de categorías
- Activar/desactivar categorías
- Asignar color e icono

---

## Estados

- **Default**: Color normal
- **Selected**: Borde highlight, background tint
- **Disabled**: Opacidad 50%

## Notas
- EyC dentro de Ocio para simplificar UI
- Ahorros funciona como "gasto" tracking (registrar transfer)
- Iconos: línea simple, 1.5px stroke

*6 Abril 2026*