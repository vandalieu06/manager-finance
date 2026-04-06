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

| Subcategoría | Icono | Color |
|--------------|-------|-------|
| Supermercado | 🛒 | brand.primary |
| Facturas | 💡 | brand.secondary |
| Transporte | 🚌 | accent.3 |
| Salud | 💊 | feedback.danger |
| Hogar | 🏠 | accent.2 |

### 2. OCIO (30%)
Wants + Essentials & Care

| Subcategoría | Icono | Color |
|--------------|-------|-------|
| Restaurantes | 🍽️ | accent.2 |
| Entretenimiento | 🎮 | accent.1 |
| Cine | 🎬 | brand.primary |
| Viajes | ✈️ | accent.3 |
| **EyC** | | |
| Higiene personal | 🧴 | feedback.info |
| Cuidado personal | 💅 | feedback.warning |
| Bebidas | ☕ | accent.2 |
| Ropa | 👕 | accent.1 |
| Snacks | 🍿 | feedback.warning |

### 3. AHORROS (20%)
Seguimiento de reservas/inversiones

| Subcategoría | Icono | Color |
|--------------|-------|-------|
| Ahorros | 💰 | feedback.success |
| Inversiones | 📈 | feedback.success |

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