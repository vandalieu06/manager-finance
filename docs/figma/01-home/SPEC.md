# SPEC - Pantalla Home (Dashboard)

> ⚠️ **IMPORTANTE**: Este SPEC refleja el estado REAL del Figma (no diseño ideal).

## Descripción General
Pantalla principal/dashboard de la app. Basada en `Final/Home Dashboard` del Figma.

---

## Apartados de la Pantalla (Según Figma)

### 1. Header
- **Logo**: "lumen" (Red Hat Mono Bold 30px, negro, subrayado azul 4px)
- **Acciones**: 2 botones icono a la derecha (44x44px, border 2px, shadow-sm)
- **Propiedades**: border-bottom 3px black, padding 16px-19px, sticky top

### 2. Bloque Principal Superior
- **Título 1**: "Bienvenido de nuevo" (Red Hat Mono Bold 40px)
- **Fecha**: "FEBRUARY 2024" (Red Hat Mono Medium 16px, azul)
- **Botón**: "Check status" (fondo blanco, border 2px, texto 20px)

### 3. Gráfico Principal
- **Tipo**: Gráfico de barras verticales geométricas
- **Categorías**: Comida, **Vaijes** (⚠️ error - debe ser "Viajes"), Tech, Bills, Otros
- **Colores**: brand.primary (Comida), accent.1 (Vaijes), feedback.warning (Tech), feedback.danger (Bills), accent.2 (Otros)
- **Labels**: Inter Bold 12px uppercase

### 4. Tarjeta de Análisis (Insight)
- **Título**: "Analysis" (Red Hat Mono Bold 48px, blanco sobre fondo azul)
- **Valor**: "24%" (feedback.danger)
- **Etiqueta**: "Alto"
- **Texto**: "Más que el mes pasado"
- **Subtexto**: "Revisar posibles mejoras"
- **Botón**: secundario "ver stats"
- **Propiedades**: fondo brand.primary, border 3px, shadow-lg 8px

### 5. Sección "INICIO"
- **Título**: "INICIO" (Red Hat Mono Bold 48px, negro)
- Separa la zona de cards estadísticas

### 6. Grid de Cards Estadísticas
- **Card 1**: "Total Spent", "$4,250.00" (card genérica con icon container)
- **Card 2-3**: Outras cards de métricas
- **Propiedades comunes**: border 3px, shadow-md, padding 30px-17px

### 7. Bottom Navigation
- **Ancho**: 370px
- **Items**: 4 tabs
- **Iconos**: casa, lista, qr/code, settings
- **Labels**: "Actividad" (repetido, ⚠️ no cerrado)
- **Estilo**: Inter Black 10px uppercase, border 4px, shadow-sm
- **Activo**: fondo azul, texto blanco
- **Inactivo**: fondo blanco, border azul, texto azul

---

## Componentes del Figma (Reales)

| Componente | propiedades |
|-------------|--------------|
| Header | border-bottom 3px, padding 16px-19px, sticky |
| Logo lumen | Red Hat Mono Bold 30px, subrayado 4px brand.primary |
| Botones icono | 44x44px, border 2px, shadow-sm |
| Botón secundario | amarillo, border 4px, shadow-md, texto 12px |
| Gráfico barras | 5 categorías, colores semánticos |
| Card análisis | fondo azul, border 3px, shadow-lg |
| Card stat | border 3px, shadow-md, padding 30px-17px |
| Bottom nav | 370px, border 4px, shadow-sm |

---

## ⚠️ Problemas a resolver

| Problema | Ubicación |
|----------|------------|
| Mezcla ES/EN | "Bienvenido de nuevo" (ES) + "Analysis", "Check status", "Total Spent" (EN) |
| Error ortográfico | "Vaijes" → "Viajes" |
| Labels no cerrados | Bottom nav dice "Actividad" repetido |
| Placeholders | "Card 01", "Total Spent" no son finales |

---

## Estados definidos en Figma
- Default: ✓ (solo este existe)

---

## Propiedades de Estilo (Unificadas)

### Tipografía
- Display/Títulos: Red Hat Mono Bold 40-48px
- Body: Red Hat Mono Medium 16-20px
- Labels: Red Hat Mono Medium 12px
- Nav: Inter Black 10px uppercase

### Colores (Tokens actualizados Figma)
- Fondo: `base.white` (#FFFFFF)
- Texto principal: `base.black` (#000000)
- Bordes: `base.black` (#000000)
- Sombras: `base.black` (#000000)
- Primary (marca): `primary.v1` (#4ECDC4) - turquesa
- Accentos: `accent1.v1` (#FFE66D), `accent2.v1` (#FF6B6B), `feedback.warning.v1` (#F59E0B), `feedback.danger.v1` (#EF4444), `feedback.info.v1` (#0EA5E9)

> ⚠️ Importante: El color de marca cambió de azul (#3B82F6) a turquesa (#4ECDC4)

### Borders & Shadows
- border-2: 2px solid black
- border-3: 3px solid black
- border-4: 4px solid black
- shadow-sm: 4px 4px 1px 0px black
- shadow-md: 4px 4px 0px 0px #111
- shadow-lg: 8px 8px 0px 0px #111

---

*6 Abril 2026 - Basado en análisis real del Figma*