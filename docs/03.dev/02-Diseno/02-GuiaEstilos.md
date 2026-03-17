# Guía de Iconos y Colores - Lumen

## Paleta de Colores para Iconos

### Colores de Tags (Font Awesome)

| Color          | Hex       | RGB                  | Uso                                              | Ejemplo                                     |
| -------------- | --------- | -------------------- | ------------------------------------------------ | ------------------------------------------- |
| **Negro/Dark** | `#1f1f29` | `rgb(31, 31, 41)`    | Categorías generales (Frontend, Backend, Design) | `<i class="fas fa-tag text-[#1f1f29]"></i>` |
| **Rojo**       | `#ff6b6b` | `rgb(255, 107, 107)` | Prioridad (Alta, Media, Baja)                    | `<i class="fas fa-tag text-[#ff6b6b]"></i>` |
| **Morado**     | `#6d5dfb` | `rgb(109, 93, 251)`  | Tecnologías y herramientas                       | `<i class="fas fa-tag text-[#6d5dfb]"></i>` |
| **Verde**      | `#32d18a` | `rgb(50, 209, 138)`  | Estado completado                                | `bg-success`                                |
| **Amarillo**   | `#ffca65` | `rgb(255, 202, 101)` | Estado pendiente                                 | `bg-warning`                                |

---

## Tipos de Tags y Sus Colores

### 1. **Categorías de Proyecto** (Negro `#1f1f29`)

- Frontend
- Backend
- Fullstack
- Design
- Mobile
- DevOps
- Testing
- Documentation

**Iconos Font Awesome sugeridos:**

- Frontend: `<i class="fas fa-desktop"></i>`
- Backend: `<i class="fas fa-server"></i>`
- Design: `<i class="fas fa-palette"></i>`
- Mobile: `<i class="fas fa-mobile-alt"></i>`

### 2. **Prioridad** (Rojo `#ff6b6b`)

- Prioridad: Alta
- Prioridad: Media
- Prioridad: Baja
- Urgente
- Crítico

**Iconos Font Awesome sugeridos:**

- Alta: `<i class="fas fa-exclamation-circle"></i>`
- Media: `<i class="fas fa-minus-circle"></i>`
- Baja: `<i class="fas fa-arrow-down"></i>`
- Urgente: `<i class="fas fa-fire"></i>`

### 3. **Tecnologías** (Morado `#6d5dfb`)

- React, forms
- Vue.js
- Angular
- Node.js
- SQL, Database
- Python
- TypeScript
- JavaScript

**Iconos Font Awesome sugeridos:**

- React: `<i class="fab fa-react"></i>`
- Vue: `<i class="fab fa-vuejs"></i>`
- Node: `<i class="fab fa-node-js"></i>`
- Python: `<i class="fab fa-python"></i>`
- Database: `<i class="fas fa-database"></i>`

---

## Iconos de Font Awesome por Categoría

### Navegación del Sidebar

```html
<!-- Dashboard -->
<i class="fas fa-chart-line text-primary"></i>

<!-- Todas las tareas -->
<i class="fas fa-list-check text-primary"></i>

<!-- Crear tarea -->
<i class="fas fa-plus text-primary"></i>
```

### Estados de Tareas

```html
<!-- Pendiente -->
<i class="fas fa-clock text-warning"></i>

<!-- En progreso -->
<i class="fas fa-spinner text-blue-500"></i>

<!-- Completado -->
<i class="fas fa-check-circle text-success"></i>

<!-- Cancelado -->
<i class="fas fa-times-circle text-red-500"></i>
```

### Acciones

```html
<!-- Editar -->
<i class="fas fa-edit text-blue-500"></i>

<!-- Eliminar -->
<i class="fas fa-trash text-red-500"></i>

<!-- Ver detalles -->
<i class="fas fa-eye text-gray-600"></i>

<!-- Duplicar -->
<i class="fas fa-copy text-gray-600"></i>

<!-- Compartir -->
<i class="fas fa-share-alt text-blue-500"></i>
```

### Usuario y Sesión

```html
<!-- Usuario -->
<i class="fas fa-user text-primary"></i>

<!-- Configuración -->
<i class="fas fa-cog text-gray-600"></i>

<!-- Cerrar sesión -->
<i class="fas fa-sign-out-alt text-red-500"></i>

<!-- Notificaciones -->
<i class="fas fa-bell text-yellow-500"></i>
```

---

## Implementación de Tags

### Estructura HTML para Tags

```html
<div class="flex items-center gap-1.5">
	<i class="fas fa-tag text-[COLOR_HEX] text-base"></i>
	<span class="text-neutral-dark text-xs font-normal">Texto del Tag</span>
</div>
```

### Ejemplos Completos

#### Tag de Categoría (Negro)

```html
<div class="flex items-center gap-1.5">
	<i class="fas fa-tag text-[#1f1f29] text-base"></i>
	<span class="text-neutral-dark text-xs font-normal">Frontend</span>
</div>
```

#### Tag de Prioridad (Rojo)

```html
<div class="flex items-center gap-1.5">
	<i class="fas fa-tag text-[#ff6b6b] text-base"></i>
	<span class="text-neutral-dark text-xs font-normal">Prioridad: Alta</span>
</div>
```

#### Tag de Tecnología (Morado)

```html
<div class="flex items-center gap-1.5">
	<i class="fas fa-tag text-[#6d5dfb] text-base"></i>
	<span class="text-neutral-dark text-xs font-normal">React, forms</span>
</div>
```

---

## Estilos CSS Personalizados (Opcional)

Si quieres crear clases reutilizables en tu `tailwind.config.js`:

```javascript
extend: {
  colors: {
    'tag-category': '#1f1f29',  // Negro para categorías
    'tag-priority': '#ff6b6b',  // Rojo para prioridad
    'tag-tech': '#6d5dfb',      // Morado para tecnologías
  }
}
```

Uso:

```html
<i class="fas fa-tag text-tag-category"></i>
<i class="fas fa-tag text-tag-priority"></i>
<i class="fas fa-tag text-tag-tech"></i>
```

---

## Recursos

- **Font Awesome Icons**: https://fontawesome.com/icons
- **CDN**: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css
- **Búsqueda de iconos**: https://fontawesome.com/search

---

## Checklist de Implementación

- [x] Font Awesome CDN añadido al HTML
- [x] Navegación convertida a checkboxes
- [x] Tags con iconos de Font Awesome
- [x] Paleta de colores establecida
- [x] Iconos con colores correctos (#1f1f29, #ff6b6b, #6d5dfb)

---

**Última actualización**: 11 de diciembre de 2025
