# SPEC - Pantalla Escanear Facturas

## Descripción General
Pantalla para registrar tickets de compra, ya sea mediante OCR (escaneo de imagen) o entrada manual. Es la funcionalidad principal de la app para registrar gastos.

## Propósito
- Permitir al usuario registrar gastos de forma rápida
- Extraer automáticamente productos de tickets mediante OCR
- Mantener historial de todos los tickets escaneados

---

## Apartados de la Pantalla

### 1. Header
- **Título**: "Escanear" o "Nuevo ticket"
- **Acción derecha**: Icono de historial (ver tickets anteriores)

### 2. Modo de Entrada (Selector)
Dos opciones claras para introducir datos:

| Modo | Icono | Descripción |
|------|-------|-------------|
| Cámara/Foto | 📷 | Subir imagen de ticket |
| Manual | ✏️ | Introducir productos manualmente |

**Diseño**: Dos botones grandes o tab toggle para seleccionar modo

### 3. Área de Captura (Modo Cámara)

#### 3.1 Upload de Imagen
- **Zona de upload**: Área grande arrastrable/seteable
- **Botón**: "Seleccionar imagen" o "Tomar foto"
- **Opciones**:
  - Galería (seleccionar imagen existente)
  - Cámara (tomar nueva foto)

#### 3.2 Preview
- **Vista previa**: Imagen del ticket seleccionada
- **Acciones**: 
  - Retake (volver a tomar/seleccionar)
  - Crop (recortar si necesita)
  - Rotate (rotar si necesita)

#### 3.3 Procesamiento (OCR)
- **Estado**: "Procesando ticket..."
- **Indicador**: Spinner o progress bar
- **Resultado**: Lista de productos detectados

#### 3.4 Resultados OCR
Lista de productos extraídos:
- **Producto detectado**: Nombre (editable)
- **Precio**: Importe (editable)
- **Cantidad**: Si detecta múltiplos
- **Acción por item**: Editar, Eliminar
- **Acción global**: Añadir producto, Añadir todos

### 4. Formulario Manual (Modo Manual)

#### Campos del formulario:
| Campo | Tipo | Requerido |
|-------|------|-----------|
| Tienda/Establecimiento | Texto | Sí |
| Fecha | Date picker | Sí |
| Productos | Lista dinámica | Sí |
| Importe total | Número | Auto/Manual |

#### Añadir Producto (Lista dinámica)
- **Producto**: Nombre del producto
- **Precio**: Importe unitario
- **Cantidad**: Número (default 1)
- **Categoría**: Selector (obligatorio) → Ver `00-categorias/SPEC.md`
- **Acción**: Añadir otro producto / Eliminar

**Botón**: "+ Añadir producto"

> **Categorías**: Usar sistema 50/30/20 (Obligación/Ocio/Ahorros)

### 5. Resumen y Guardado

#### Datos del Ticket:
- Tienda
- Fecha
- Importe total (suma automática de productos)
- Número de productos

#### Acciones:
- **Guardar**: Guardar ticket y volver a Home
- **Guardar y añadir otro**: Mantener pantalla para nuevo ticket
- **Cancelar**: Descartar y volver

---

## Sub-Pantallas

### 1. Historial de Tickets
**Acceso**: Icono en header

**Contenido:**
- Lista de tickets anteriores
- Cada item muestra:
  - Fecha
  - Tienda
  - Importe total
  - Número de productos
- Buscador/filtrar por fecha
- Click para ver detalle

### 2. Detalle de Ticket
**Acceso**: Click en item del historial

**Contenido:**
- Imagen del ticket (si existe)
- Datos: tienda, fecha, importes
- Lista de productos
- Acciones: Editar, Eliminar, Duplicar

### 3. Editar Productos
**Acceso**: Desde resultados OCR o ticket existente

**Contenido:**
- Lista editable de productos
- Editar: nombre, precio, cantidad, categoría
- Añadir nuevo producto
- Eliminar producto

---

## Componentes Específicos Requeridos

### Mode Selector (Cámara/Manual)
```
┌─────────────────────────────┐
│   [📷 Cámara]  [✏️ Manual] │
└─────────────────────────────┘
```

### Upload Zone
```
┌─────────────────────────────┐
│                             │
│      📷 Seleccionar        │
│    imagen o tomar foto     │
│                             │
│   [Galería]    [Cámara]    │
└─────────────────────────────┘
```

### Product Item (Editable)
```
┌─────────────────────────────┐
│ [x] Leche                  │
│    €2.50    ×1   [🗑]      │
└─────────────────────────────┘
```

### Manual Product Form
```
┌─────────────────────────────┐
│ Producto: [____________]    │
│ Precio:   [____________]    │
│ Cantidad: [___] [Añadir]   │
└─────────────────────────────┘
```

### Ticket Summary Card
```
┌─────────────────────────────┐
│ Carrefour          06/04/26 │
│ 5 productos        €45,20   │
└─────────────────────────────┘
```

---

## Estados de la Pantalla

### Estado: Selector de modo
El usuario elige cómo introducir datos.

### Estado: Cámara activa
- Viewfinder de cámara
- Guía de alineación

### Estado: Imagen seleccionada
- Preview de la imagen
- Botones de acción (procesar, retake)

### Estado: Procesando (OCR)
- Spinner/loader
- Mensaje: "Extrayendo productos..."
- **Importante**: Este estado requiere manejo offline/online

### Estado: Resultados OCR (edición)
- Lista de productos detectados
- Cada uno editable
- Posibilidad de añadir/eliminar

### Estado: Formulario manual
- Campos vacíos o con datos previos
- Validación en tiempo real

### Estado: Guardando
- Spinner
- Evitar doble tap

### Estado: Éxito
- Feedback visual (check, toast)
- Navegar a Home o limpiar para nuevo

### Estado: Error
- Mensaje de error
- Opción de reintentar
- Si OCR falla: ofrecer entrada manual

---

## Estados Vacíos y Edge Cases

### Ticket vacío (sin productos)
- Mensaje: "No se detectaron productos"
- Opción: Introducir manualmente

### OCR parcialmente exitoso
- Algunos productos detectados, otros no
- Suggestión: "Revisa los productos detectados"

### Imagen no legible
- Mensaje: "No se pudo leer el ticket"
- Sugerencia: "Prueba con una foto más clara" o "Introdúcelo manualmente"

---

## Consideraciones de Diseño

### Neobrutalismo
- Botones grandes y claros
- Espaciado generoso
- Bordes visibles en zonas de input

### Colores (Tokens Figma)
- Fondo: `base.white` (#FFFFFF)
- Texto: `base.black` (#000000)
- Primary: `primary.v1` (#4ECDC4) - turquesa
- Éxito: `feedback.success.v1` (#22C55E)
- Error: `feedback.danger.v1` (#EF4444)
- Warning: `feedback.warning.v1` (#F59E0B)
- Info: `feedback.info.v1` (#0EA5E9)
- Categorías: `category_obligacion.v1`, `category_ocio.v1`, `category_ahorro.v1`

> ⚠️ Importante: Primary cambió de azul a turquesa (#4ECDC4)

### UX - Flujo Natural
1. Seleccionar modo → 2. Introducir datos → 3. Revisar → 4. Guardar

### Feedback continuo
- Siempre saber en qué paso estamos
- Loading states claros
- Confirmaciones de acciones

### Manejo Offline
- OCR puede no funcionar offline (requiere API)
- Indicador claro de modo online/offline
- Guardado local siempre disponible

---

## Flujo de Usuario

```
[Escanear Facturas]
│
├── [Cámara]
│   ├── Seleccionar imagen
│   │   ├── Galería → Preview → Procesar
│   │   └── Cámara → Preview → Procesar
│   ├── Procesar (OCR)
│   │   ├── Éxito → Editar productos → Guardar
│   │   └── Fallo → Mensaje → Manual
│   └── Guardar → Home
│
├── [Manual]
│   ├── Rellenar formulario
│   ├── Añadir productos (1..n)
│   └── Guardar → Home
│
└── [Historial]
    ├── Ver lista de tickets
    └── Click ticket → Detalle → Editar/Eliminar
```

---

## Notas de Implementación React Native

- **Cámara**: `react-native-camera` o `react-native-vision-camera`
- **Image Picker**: `react-native-image-picker`
- **OCR**: Integración con API (OpenAI, Google Vision, etc.)
- **Formularios**: `react-hook-form` o similar
- **Keyboard**: `KeyboardAvoidingView` para formularios largos

---

## Referencias

- Funcionalidad OCR: `docs/01.manual/1. Definición proyecto.md`
- Diseño tokens: `docs/03.dev/02-Diseno/02-GuiaEstilos.md`

---

*Especificación creada: 6 de Abril de 2026*
*Versión: 1.0*