# SPEC - Pantalla Productos

> ⚠️ **IMPORTANTE**: Este SPEC refleja el estado REAL del Figma (no diseño ideal).

## Descripción General
Pantalla secundaria de exploración/listado. Basada en `Final/productos` del Figma.

---

## Apartados de la Pantalla (Según Figma)

### 1. Header
- **Logo**: "lumen" (Red Hat Mono Bold 30px)
- **Acciones**: 2 botones icono a la derecha (44x44px)
- **Propiedades**: idéntico al Home

### 2. Título Principal
- **Texto**: "Productos" (Red Hat Mono Bold 48px, negro)

### 3. Input de Búsqueda
- **Componente más maduro del Figma**
- **Dimensiones**: 358px x 69px (total), caja interna 40px height
- **Label**: "input" (Red Hat Mono 18px, negro)
- **Caja**: border 4px solid black, padding 8px 12px
- **Icono**: 24x24px a la izquierda
- **Placeholder**: Red Hat Mono 18px, color gris #404040

### 4. Grupo de Botones (Filtros/Acciones)
- **3 botones horizontales** debajo del input
- **Estilo**: rectangulares, alto contraste
- **Etiquetas vistas**: "Primario" (⚠️ placeholder)
- **Iconos**: diversos según función

### 5. Bloque de Cards (Resumen)
- **1 card grande** arriba
- **2 cards pequeñas** debajo
- **Estilo**: mismo patrón que cards del dashboard

### 6. Sección "Lo más gastado"
- **Título**: "Lo más gastado" (icono + texto)
- **Función**: marca inicio de ranking

### 7. Lista de Items (Ranking)
- **Componente**: `itemLista`
- **Estructura**: fila horizontal, icono izquierda, texto derecha
- **Dimensiones**: ~350px width, 50px height
- **Iconos detectados**:
  - developer_board
  - computer
  - keyboard
  - mouse
- **⚠️ Problema**: iconos parecen tecnológicos, no financieros

### 8. Bottom Navigation
- Mismo patrón que Home (370px, 4 tabs, labels "Actividad" repetidos)

---

## Componentes del Figma (Reales)

| Componente | Propiedades |
|------------|-------------|
| Input con label | 358x69px, border 4px, label 18px, placeholder 18px |
| Button large | ~48px height, rectangular, border |
| List Item | 350x50px, icono 24px |
| Cards | Mismo estilo que dashboard |

---

## ⚠️ Problemas a resolver

| Problema | Ubicación |
|----------|------------|
| Semántica | No queda claro si "Productos" = productos comprados, gastos, categorías |
| Iconos lista |computer, keyboard, mouse parecen tecnológicos, no financieros |
| Labels botones | "Primario" es placeholder |
| Placeholders | Varios textos no son finales |

---

## Propiedades de Estilo (Unificadas)

### Input más maduro
```
- width: 358px
- height: 69px
- label: Red Hat Mono 18px
- caja: 40px height, border 4px solid black
- padding: 8px 12px
- gap: 10px
- icono: 24x24px
- placeholder: #404040
```

### List Item
```
- width: ~350px
- height: 50px
- icono: 24px
- padding lateral visible
```

---

### Colores (Tokens actualizados Figma)
- Fondo: `base.white` (#FFFFFF)
- Texto: `base.black` (#000000)
- Bordes: `base.black` (#000000)
- Primary: `primary.v1` (#4ECDC4) - turquesa
- Placeholder: #404040

> ⚠️ Importante: El color de marca cambió de azul a turquesa (#4ECDC4)

---

*6 Abril 2026 - Basado en análisis real del Figma*