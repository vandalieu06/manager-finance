# Tareas de Figma - Proyecto Lumen (Manager Finance)

## Resumen
Lista de tareas con checkbox. Marcar [x] cuando esté hecho.

**Estado real del Figma:** 2 pantallas existentes (Home Dashboard, Productos)

---

## FASE 1: Setup y Fundamentos

### 1.1 Configuración Archivo Figma
- [x] ✅ Archivo Figma existe (Manager Finance)
- [x] ✅ 2 pantallas reales: Home Dashboard, Productos

### 1.2 Design Tokens - UNIFICADOS SEGÚN FIGMA

#### 📝 Tipografía (según análisis Figma)

| Token | Familia | Uso | Peso | Tamaño |
|-------|---------|-----|------|--------|
| `font-display` | Red Hat Mono | Branding, títulos, métricas, labels | Bold (700) | 30-48px |
| `font-body` | Red Hat Mono | Cuerpo, labels medianos, texto general | Medium (500) | 16-20px |
| `font-label` | Red Hat Mono | Labels pequeñas, textos secundarios | Medium (500) | 12px |
| `font-nav` | Inter | Navegación inferior | Black (900) | 10px uppercase |
| `font-chart` | Inter | Etiquetas del gráfico | Bold (700) | 12px uppercase |

**Regla unificada:** 
- ✅ **Red Hat Mono** para todo excepto navegación e labels de gráfico
- ✅ **Inter** solo para nav y gráfico

#### 🎨 Colores (según análisis Figma)

| Token | Valor | Uso |
|-------|-------|-----|
| `white` | `#FFFFFF` | Fondo principal |
| `black` | `#000000` | Texto, bordes |
| `black-soft` | `#111111` | Sombras |
| `brand.primary` | `#3B82F6` | Acento principal, botones icono, nav activo |
| `brand.secondary` | `#FFFF00` | Botón secundario |
| `accent.1` | `#00FF00` | Barra gráfico (Vaijes) |
| `accent.2` | `#EC4899` | Barra gráfico (Otros), tarjeta rosa |
| `accent.3` | `#06B6D4` | (cyan) |
| `feedback.success` | `#22C55E` | Botones icono verde, texto positivo |
| `feedback.warning` | `#F59E0B` | Barra gráfico Tech |
| `feedback.danger` | `#EF4444` | Barra Bills, tarjeta roja, comparación negativa |
| `feedback.info` | `#0EA5E9` | Tarjeta azul inferior |

#### 📏 Spacing (según análisis Figma)

| Token | Valor |
|-------|-------|
| `space-1` | 4px |
| `space-2` | 8px |
| `space-3` | 12px |
| `space-4` | 16px |
| `space-5` | 20px |
| `space-6` | 24px |
| `space-7` | 32px |
| `space-8` | 40px |

#### ⬜ Borders (según análisis Figma)

| Token | Valor |
|-------|-------|
| `border-2` | 2px solid black |
| `border-3` | 3px solid black |
| `border-4` | 4px solid black |

**Regla:** Todos los bordes son black, sin excepciones.

#### 🌑 Sombras (según análisis Figma)

| Token | Valor |
|-------|-------|
| `shadow-sm` | 4px 4px 1px 0px black |
| `shadow-md` | 4px 4px 0px 0px #111 |
| `shadow-lg` | 8px 8px 0px 0px #111 |

**Regla:** Sombras duras, negras, sin blur decorativo (brutalismo puro).

#### ⭕ Border Radius

| Token | Valor |
|-------|-------|
| `radius-none` | 0px |

**Regla:** Sistema angular y rígido. Sin redondeados.

---

## FASE 2: Componentes Base - ✅ HECHOS EN FIGMA

### 2.1 Botones
- [x] ✅ Button Icon (44x44px, border 2px, shadow-sm)
- [x] ✅ Button Secondary (amarillo, border 4px, shadow-md)
- [x] ✅ Button Primary (brand.primary)

### 2.2 Inputs
- [x] ✅ Input con label (358x69px, label 18px, caja 40px, border 4px)

### 2.3 Navegación
- [x] ✅ Header (border-bottom 3px black, padding 16px-19px, sticky)
- [x] ✅ Bottom Navigation (370px, border 4px, shadow-sm, 4 items)

### 2.4 Contenedores
- [x] ✅ Card Dashboard (border 3px, shadow-md, padding 30px-17px)
- [x] ✅ Card Análisis (fondo azul, border 3px, shadow-lg)
- [x] ✅ Card Stat (icon container 2px, label 12px, valor 40px)

### 2.5 Datos
- [x] ✅ List Item / Ranking Item (350px width, 50px height)

### 2.6 Gráficos
- [x] ✅ Gráfico de barras (categorías: Comida, Vaijes, Tech, Bills, Otros)

---

## FASE 3: Componentes de Negocio

### 3.1 Dashboard y Gráficos
- [x] ✅ Stat Card (métricas rápidas)
- [x] ✅ Trend Indicator (Análisis + 24% + "Más que el mes pasado")

### 3.2 Productos
- [x] ✅ Product Card (cards destacadas)
- [x] ✅ Product List Item (ítems con iconos)
- [x] ✅ Filter Buttons (3 botones horizontales)

---

## FASE 4: Pantallas

### 4.1 Home (Dashboard) ✅ HECHO
- [x] ✅ Header con logo "lumen" + 2 botones icono
- [x] ✅ Bloque "Bienvenido de nuevo" + "FEBRUARY 2024" + "Check status"
- [x] ✅ Gráfico de barras por categorías (Comida, Vaijes, Tech, Bills, Otros)
- [x] ✅ Tarjeta de análisis ("Analysis", 24%, "Alto", "Más que el mes pasado")
- [x] ✅ Grid de cards estadísticas (Total Spent, $4,250.00)
- [x] ✅ Bottom Navigation (4 tabs: Actividad repetido, iconos: casa, lista, qr, settings)
- [x] ✅ Título sección "INICIO"

### 4.2 Productos ✅ HECHO
- [x] ✅ Header (lumen + iconos)
- [x] ✅ Título "Productos"
- [x] ✅ Input de búsqueda con label
- [x] ✅ 3 botones de filtro/acción
- [x] ✅ Bloque de cards (1 grande + 2 pequeñas)
- [x] ✅ Sección "Lo más gastado" con lista de items
- [x] ✅ Bottom Navigation

### 4.3 Configuración ⚠️ PENDIENTE - NO EXISTE EN FIGMA
- [ ] Por crear en Figma
- [ ] Header
- [ ] Perfil usuario
- [ ] Ajustes (moneda, notificaciones, categorías)
- [ ] Datos (exportar, importar, eliminar cuenta)
- [ ] Información (versión, términos, privacidad)
- [ ] Ayuda/FAQ

### 4.4 Escanear Facturas ⚠️ PENDIENTE - NO EXISTE EN FIGMA
- [ ] Por crear en Figma
- [ ] Header
- [ ] Mode Selector (Cámara/Manual)
- [ ] Upload Zone
- [ ] Processing OCR
- [ ] Resultados editable
- [ ] Historial

---

## FASE 5: Categorías (50/30/20)

### Estructura ✅ SPEC CREADO
- [x] ✅ Obligación (50%): Supermercado, Facturas, Transporte, Salud, Hogar
- [x] ✅ Ocio (30%): Restaurantes, Entretenimiento, Cine, Viajes, EyC
- [x] ✅ Ahorros (20%): Transfers, inversiones

### Componentes de Categorías
- [ ] Category Badge
- [ ] Category Selector
- [ ] Filter Chips
- [ ] Budget Progress Widget

---

## FASE 6: Prototipado

- [ ] Flujo Registro/Login
- [ ] Flujo Escanear ticket
- [ ] Flujo Productos → filtrar
- [ ] Transiciones

---

## FASE 7: Revisión y Polish

### ⚠️ Problemas detectados en Figma (por resolver)

| Problema | Descripción | Estado |
|----------|-------------|--------|
| **Idioma** | Mezcla ES/EN en títulos, labels, categorías | ❌ PENDIENTE |
| **Naming** | Dualidad "Lumen" (branding) vs "Manager Finance" (archivo) | ❌ PENDIENTE |
| **Errores ortográficos** | "Vaijes" → debería ser "Viajes" | ❌ PENDIENTE |
| **Labels nav** | Textos no cerrados ("Actividad" repetido) | ❌ PENDIENTE |
| **Placeholders** | "Card 01", "Total Spent", "Primario" no son finales | ❌ PENDIENTE |
| **Estados inputs** | No definidos (hover, focus, error, disabled) | ❌ PENDIENTE |
| **Categorías gráfico** | Mezcla ES/EN (Tech, Bills, Otros) | ❌ PENDIENTE |

---

## 📊 Resumen de Estado

```
FASE 1: Setup         ████████████ 100% (tokens unificados)
FASE 2: Base         ████████████ 100% (componentes hechos en Figma)
FASE 3: Negocio      ████████████ 100% (dashboard/productos hechos)
FASE 4: Pantallas    ██████░░░░░░  50% (2/4: Home + Productos hechos)
FASE 5: Categorías   ████░░░░░░░░  20% (SPEC creado, componentes pending)
FASE 6-7: Polish     ░░░░░░░░░░░░   0%
```

---

## 📋 Checklist de Correcciones Necesarias

### Idioma → Unificar a ESPAÑOL
- [ ] "Check status" → "Ver estado" o similar
- [ ] "Analysis" → "Análisis"
- [ ] "Total Spent" → "Total gastado"
- [ ] "Products" → "Productos" (ya está)
- [ ] "Card 01" → eliminar o substituir
- [ ] "Check status" → texto final

### Errores → Corregir
- [ ] "Vaijes" → "Viajes"

### Naming → Decidir
- [ ] ¿Usar "Lumen" o "Manager Finance" como nombre final?

### Labels nav → Cerrar
- [ ] 4 labels finales para bottom navigation

---

*6 Abril 2026 - Actualizado con análisis estético del Figma*