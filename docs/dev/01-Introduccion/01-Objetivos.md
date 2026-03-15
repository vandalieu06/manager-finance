# Lumen - Gestor de Tareas Educativo

## Objetivo del Proyecto

Crear una interfaz web intuitiva y visualmente atractiva que permita:
- Gestionar tareas con diferentes estados (Pendiente, En progreso, Completado)
- Filtrar tareas por categoría, prioridad y estado
- Crear nuevas tareas con información detallada
- Visualizar estadísticas de progreso
- Mantener sesiones de usuario con localStorage

## Arquitectura del Proyecto

### Stack Tecnológico

- **Frontend**: HTML5 puro (sin frameworks)
- **Estilos**: Tailwind CSS (CDN) con tokens de diseño personalizados
- **Iconografía**: Font Awesome 6.5.1
- **Tipografía**: Google Fonts - Inter (weights: 400, 600, 700, 800)
- **Lógica**: TypeScript compilado a JavaScript
- **Almacenamiento**: localStorage (temporal, pendiente migración a base de datos)

### Estructura de Archivos

```
mangaer-tasks/
├── login.html                    # Página de inicio de sesión
├── signup.html                   # Página de registro
├── index.html                    # Dashboard principal
├── todasLasTareas.html          # Vista completa de tareas con filtros
├── crearTarea.html              # Formulario de creación de tareas
├── src/
│   ├── index.css                # Estilos globales
│   ├── main.tsx                 # Entry point (no usado actualmente)
│   ├── assets/
│   │   ├── logoJV.png          # Logo de la escuela (222x114px)
│   │   └── logoMarcaSVG.svg    # Logo vectorial de la marca
│   └── components/
│       └── LoginPage.tsx        # Componente React (no usado)
├── TS/
│   ├── login.ts                 # Lógica de autenticación
│   ├── signup.ts                # Lógica de registro
│   └── script.ts                # Lógica general (sesión, tareas)
├── dist/
│   ├── login.js                 # login.ts compilado
│   ├── signup.js                # signup.ts compilado
│   └── script.js                # script.ts compilado
├── tailwind.config.js           # Configuración de tokens de diseño
├── tsconfig.json                # Configuración de TypeScript
├── package.json                 # Dependencias del proyecto
├── DESIGN_IMPLEMENTATION.md     # Documentación de implementación de diseño
└── ICON_COLOR_GUIDE.md         # Guía de iconos y colores
```

## Sistema de Diseño

### Paleta de Colores

El proyecto utiliza un sistema de colores consistente definido en `tailwind.config.js`:

```javascript
colors: {
    primary: {
        DEFAULT: '#6d5dfb',    // Púrpura principal
        dark: '#362c77',       // Púrpura oscuro
    },
    neutral: {
        light: '#f7f7fb',      // Fondo claro
        medium: '#d4d4e0',     // Gris medio (disabled/cards)
        dark: '#1f1f29',       // Negro texto/bordes
    },
    warning: '#ffca65',        // Amarillo (estado Pendiente)
    success: '#32d18a',        // Verde (estado Completado)
}
```

### Sistema de Espaciado

Tokens de espaciado personalizados:

| Token | Valor | Uso |
|-------|-------|-----|
| `spacerxs` | 4px | Border radius pequeño |
| `spacers` | 8px | Gaps pequeños, padding mínimo |
| `spacerm` | 16px | Padding estándar, gaps medios |
| `spacerx` | 24px | Títulos, botones grandes |
| `spacerxl` | 32px | Subtítulos |
| `spacerxxl` | 40px | Encabezados principales |

### Tipografía

- **Familia**: Inter (Google Fonts)
- **Pesos disponibles**: 400 (Regular), 600 (Semi Bold), 700 (Bold), 800 (Extra Bold)
- **Tamaños principales**:
  - Títulos principales: 40px (font-bold)
  - Subtítulos: 32px (font-normal)
  - Botones: 24px (font-semibold/extrabold)
  - Texto normal: 16px (font-normal)

### Sistema de Iconos

**Font Awesome 6.5.1** con esquema de colores semántico:

| Color | Hex | Uso |
|-------|-----|-----|
| Negro | `#1f1f29` | Categorías (Frontend, Backend, Database) |
| Rojo | `#ff6b6b` | Prioridad (Alta, Media, Baja) |
| Púrpura | `#6d5dfb` | Tecnologías (React, SQL, etc.) |

**Ejemplo de uso**:
```html
<!-- Tag de categoría -->
<i class="fas fa-tag text-[#1f1f29]"></i>
<span>Frontend</span>

<!-- Tag de prioridad -->
<i class="fas fa-tag text-[#ff6b6b]"></i>
<span>Prioridad: Alta</span>

<!-- Tag de tecnología -->
<i class="fas fa-tag text-[#6d5dfb]"></i>
<span>React, forms</span>
```

## Páginas y Funcionalidades

### 1. login.html - Página de Inicio de Sesión

**Diseño**:
- Layout de 2 columnas
- Columna izquierda: Logo de la escuela (logoJV.png)
- Separador vertical (borde negro 2px)
- Columna derecha: Logo de marca (logoMarcaSVG.svg) + formulario

**Campos**:
- Usuario (input de 66px altura)
- Contraseña (input de 66px altura)
- Botón "Entrar" (púrpura, 24px font-semibold)

**Lógica** (`dist/login.js`):
```typescript
function validarUsuario(username: string, password: string) {
    // Validación contra localStorage
    // Si válido: guarda "usuariActual" y redirige a index.html
    // Si inválido: muestra error
}
```

**Protección**: Ninguna (página pública)

---

### 2. signup.html - Página de Registro

**Diseño**: Similar a login.html con más campos

**Campos**:
- Nombre y Apellidos (grid 2 columnas)
- Email
- Username
- Password
- Botón "Registrar"

**Lógica** (`dist/signup.js`):
```typescript
function crearUsuario(userData: UserData) {
    // Crea usuario en localStorage
    // Redirige a login.html
}
```

**Protección**: Ninguna (página pública)

---

### 3. index.html - Dashboard Principal

**Layout**:
- **Sidebar izquierdo (200px)**:
  - Logo de la escuela
  - 3 opciones de navegación con checkboxes:
    - Dashboard
    - Todas las tareas
    - Crear tarea (con icono `fa-plus`)
  - Separador
  - Estadísticas:
    - Tareas totales: 24
    - Completadas: 12

- **Contenido principal**:
  - Encabezado: "Dashboard" + "Revisa tus tareas"
  - Botón "Opciones"
  - 3 tarjetas de estadísticas (grid-cols-3):
    - 24 total
    - 8 en progreso
    - 12 completadas
  - Sección "Tareas recientes" con 3 tarjetas de tareas

**Estructura de Tarjeta de Tarea**:
```html
<article class="bg-neutral-light border-2 border-primary-dark rounded-lg p-4">
    <h3 class="text-2xl font-bold">Título de la tarea</h3>
    <p class="text-base font-normal">Descripción</p>
    <div class="flex gap-2">
        <!-- Tags con iconos Font Awesome -->
        <i class="fas fa-tag text-[#1f1f29]"></i><span>Frontend</span>
        <i class="fas fa-tag text-[#ff6b6b]"></i><span>Prioridad: Alta</span>
        <i class="fas fa-tag text-[#6d5dfb]"></i><span>React, forms</span>
    </div>
    <span class="bg-warning">Pendiente</span> <!-- o bg-success para Completado -->
</article>
```

**Protección**: Requiere `localStorage.getItem("usuariActual")`

---

### 4. todasLasTareas.html - Vista de Todas las Tareas con Filtros

**Layout de 3 columnas**:

#### Columna 1 - Sidebar Izquierdo (335px)
- Logo de la escuela (162px altura)
- Navegación con checkboxes (igual que index.html)
- Separador
- Estadísticas (igual que index.html)

#### Columna 2 - Panel de Filtros (335px)
- **Sección Categorías**:
  ```html
  <h3>Categorias</h3>
  <div>Frontend (20)</div>
  <div>Backend (16)</div>
  <div>Database (4)</div>
  ```

- **Sección Prioridad**:
  ```html
  <h3>Prioridad</h3>
  <div>Alta</div>
  <div>Media</div>
  <div>Baja</div>
  ```

- **Sección Estado**:
  ```html
  <h3>Estado</h3>
  <div>Pendiente</div>
  <div>En progreso</div>
  <div>Completado</div>
  ```

- **Botón "Limpiar filtros"** (inferior):
  - Fondo púrpura, texto blanco
  - 24px font-extrabold
  - Borde 4px púrpura
  - Rounded-2xl

#### Columna 3 - Lista de Tareas (flex-1)
- **Fondo**: `bg-neutral-medium` (#d4d4e0)
- **Borde**: 2px `border-primary-dark`

**Elementos**:
1. **Barra de búsqueda** (66px altura):
   ```html
   <div class="flex gap-6">
       <div class="flex-1 bg-neutral-light">
           <i class="fas fa-search"></i>
           <span>buscar</span>
       </div>
       <button class="bg-primary">Crear nueva tarea</button>
   </div>
   ```

2. **Lista scrolleable de tareas**:
   - 6 tarjetas de tareas (mismo diseño que index.html)
   - Gap de 17px entre tarjetas
   - Overflow-y-auto para scroll

**Protección**: Requiere sesión

---

### 5. crearTarea.html - Formulario de Creación de Tareas

**Layout**: Sidebar izquierdo (335px) + formulario principal

**Encabezado del formulario**:
```html
<div class="bg-neutral-light p-4">
    <h1 class="text-[40px] font-bold">Crear nueva tarea</h1>
    <p class="text-[32px] font-normal">Llena los campos para la nueva tarea</p>
</div>
<div class="border-t-4 border-primary-dark"></div>
```

**Campos del formulario**:

1. **Nombre de la tarea**:
   - Input de 66px altura
   - Ancho: 551px
   - Placeholder: "Nombre"

2. **Descripción**:
   - Textarea de 231px altura
   - Ancho: 551px
   - Placeholder: "Describe la tarea aquí...."

3. **Categoría** (grid 5 columnas):
   - Botones: Frontend, Backend, Database, Learning, "Añadir otra..."
   - Altura: 124px cada uno
   - Borde: 2px `border-primary`
   - Hover: `bg-primary` + `text-white`

4. **Prioridad** (grid 3 columnas):
   - Botones: Alta, Media, Baja
   - Altura: 124px cada uno
   - Mismo estilo que categoría

5. **Tags**:
   - Input de 66px altura
   - Ancho: 551px
   - Placeholder: "Con la coma separas las categorias"

6. **Fecha de entrega**:
   - Input de 66px altura
   - Ancho: 551px
   - Placeholder: "dd/mm/yyyy"

**Botones de acción**:
```html
<button type="submit" class="bg-primary text-2xl">Crear nueva tarea</button>
<button type="button" class="border-2 border-primary text-2xl" onclick="window.history.back()">
    Cancelar
</button>
```

**Protección**: Requiere sesión

---

## Sistema de Autenticación

### Flujo de Sesión

1. **Inicio**: Todas las páginas protegidas ejecutan verificación en `window.onload`
2. **Verificación**: Se busca `localStorage.getItem("usuariActual")`
3. **Redirect**: Si no existe, `window.location.href = "login.html"`
4. **Persistencia**: La sesión permanece hasta que se ejecuta `tancarSesio()`

### Código de Protección (en script.ts)

```typescript
window.onload = function () {
    const usuariActual = localStorage.getItem("usuariActual");
    
    if (!usuariActual) {
        window.location.href = "login.html";
    }
    
    // Cargar tareas del usuario
    const tasques = JSON.parse(localStorage.getItem("tasques") || "[]") as tarea[];
}
```

### Función de Cierre de Sesión

```typescript
function tancarSesio() {
    localStorage.removeItem("usuariActual");
    window.location.href = "login.html";
}
```

**Botón de cierre** (presente en todas las páginas protegidas):
```html
<button onclick="tancarSesio()" 
        class="fixed bottom-6 right-6 bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg">
    Tancar Sessió
</button>
```

---

## Modelo de Datos

### Interface: Tarea (TypeScript)

```typescript
interface tarea {
    titulo: string;           // Título de la tarea
    descripcion?: string;     // Descripción opcional
    estado: number;           // 1: Pendiente, 2: En progreso, 3: Completado
    fecha?: Date;            // Fecha de entrega opcional
    prioridad: number;       // 1: Alta, 2: Media, 3: Baja
    etiquetas: string[]      // Array de tags (ej: ["React", "forms"])
}
```

### Estados de Tarea

| Valor | Estado | Color Badge | Clase CSS |
|-------|--------|-------------|-----------|
| 1 | Pendiente | Amarillo | `bg-warning` (#ffca65) |
| 2 | En progreso | (No mostrado en diseño actual) | - |
| 3 | Completado | Verde | `bg-success` (#32d18a) |

### Prioridades

| Valor | Nivel | Color Tag |
|-------|-------|-----------|
| 1 | Alta | Rojo (#ff6b6b) |
| 2 | Media | Rojo (#ff6b6b) |
| 3 | Baja | Rojo (#ff6b6b) |

### Categorías Predefinidas

- **Frontend**: Color negro en tags
- **Backend**: Color negro en tags
- **Database**: Color negro en tags
- **Learning**: Color negro en tags

---

## Funcionalidades Principales

### 1. Crear Tarea

**Archivo**: `TS/script.ts` → `crearTarea()`

```typescript
function crearTarea(
    titulo: string,
    descripcion?: string,
    estado: number = 1,
    fecha?: Date,
    prioridad: number = 1,
    etiquetas: string[] = [] 
) {
    const tasques = JSON.parse(localStorage.getItem("tasques") || "[]") as tarea[];
    
    const novaTarea: tarea = {
        titulo,
        descripcion,
        estado,
        fecha,
        prioridad,
        etiquetas
    };
    
    tasques.push(novaTarea);
    localStorage.setItem("tasques", JSON.stringify(tasques));
}
```

**Estado actual**: ⚠️ Almacena en localStorage (temporal)
**Pendiente**: Migrar a base de datos con API

### 2. Listar Tareas

**Lógica**:
```typescript
window.onload = function () {
    const tasques = JSON.parse(localStorage.getItem("tasques") || "[]") as tarea[];
    // Renderizar tareas en el DOM
}
```

**Renderizado**: Actualmente las tareas están hardcodeadas en el HTML
**Pendiente**: JavaScript dinámico para renderizar desde localStorage/API

### 3. Filtrar Tareas

**Interfaz**: Panel de filtros en `todasLasTareas.html`

**Filtros disponibles**:
- Por categoría (Frontend, Backend, Database)
- Por prioridad (Alta, Media, Baja)
- Por estado (Pendiente, En progreso, Completado)

**Estado actual**: ⚠️ UI implementada, lógica de filtrado pendiente
**Pendiente**: JavaScript para filtrado reactivo

### 4. Buscar Tareas

**Interfaz**: Barra de búsqueda en `todasLasTareas.html`

**Estado actual**: ⚠️ UI implementada, funcionalidad pendiente
**Pendiente**: JavaScript para búsqueda en tiempo real

---

## Patrones de Diseño Implementados

### 1. Componentes Reutilizables

**Sidebar de Navegación** (presente en 3 páginas):
```html
<aside class="w-[335px] border-2 border-black rounded p-4">
    <!-- Logo -->
    <div class="h-[162px]">
        <img src="./src/assets/logoJV.png" />
    </div>
    
    <!-- Navegación con checkboxes -->
    <nav class="flex flex-col gap-2">
        <label class="bg-neutral-light border border-neutral-dark">
            <input type="checkbox" />
            <span>Dashboard</span>
        </label>
        <!-- ... más opciones -->
    </nav>
    
    <!-- Estadísticas -->
    <div class="flex flex-col gap-4">
        <div class="bg-neutral-light">
            <p>Tareas totales</p>
            <p>24</p>
        </div>
    </div>
</aside>
```

### 2. Tarjetas de Tarea (Task Cards)

Patrón consistente en `index.html` y `todasLasTareas.html`:

```html
<article class="bg-neutral-light border-2 border-primary-dark rounded-lg p-4 
                flex items-start justify-between hover:bg-gray-50 transition-colors">
    <!-- Contenido izquierdo -->
    <div class="flex flex-col gap-2 flex-1">
        <h3 class="text-primary-dark text-2xl font-bold">Título</h3>
        <p class="text-primary-dark text-base">Descripción</p>
        
        <!-- Tags -->
        <div class="flex gap-2 items-center flex-wrap">
            <div class="flex items-center gap-1.5">
                <i class="fas fa-tag text-[#1f1f29]"></i>
                <span>Categoría</span>
            </div>
            <!-- ... más tags -->
        </div>
    </div>
    
    <!-- Badge de estado (derecha) -->
    <span class="bg-warning px-4 py-2 text-base font-semibold shrink-0">
        Pendiente
    </span>
</article>
```

### 3. Inputs Consistentes

Todos los inputs siguen el mismo patrón:

```html
<div class="flex flex-col gap-4 w-[551px]">
    <label class="text-primary text-base font-extrabold">Label</label>
    <input 
        type="text"
        placeholder="Placeholder"
        class="bg-neutral-light border border-primary-dark rounded-lg h-[66px] 
               px-4 py-2 text-neutral-medium text-base font-extrabold 
               placeholder-neutral-medium focus:outline-none focus:ring-2 focus:ring-primary"
    />
</div>
```

**Características**:
- Altura fija: 66px
- Ancho estándar: 551px
- Borde: 1px `border-primary-dark`
- Placeholder: color `neutral-medium` (#d4d4e0)
- Focus: ring 2px púrpura

---

## Cómo Ejecutar el Proyecto

### Prerequisitos

- Node.js (para compilar TypeScript)
- Navegador web moderno
- Servidor HTTP local (opcional)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/vandalieu06/mangaer-tasks.git
cd mangaer-tasks

# Instalar dependencias
npm install
```

### Compilar TypeScript

```bash
# Compilar una vez
npm run build

# O compilar en modo watch
npx tsc --watch
```

Esto genera los archivos JS en la carpeta `dist/`:
- `TS/login.ts` → `dist/login.js`
- `TS/signup.ts` → `dist/signup.js`
- `TS/script.ts` → `dist/script.js`

### Ejecutar

#### Opción 1: Abrir directamente
Abre `login.html` en tu navegador (doble clic)

#### Opción 2: Servidor HTTP local (recomendado)
```bash
# Con Python
python -m http.server 8000

# O con Node.js http-server
npx http-server -p 8000
```

Luego navega a: `http://localhost:8000/login.html`

### Flujo de Usuario

1. **Registro**: Abre `signup.html` → Crea un usuario → Redirige a login
2. **Login**: Usa las credenciales creadas → Redirige a `index.html`
3. **Dashboard**: Visualiza estadísticas y tareas recientes
4. **Ver todas**: Navega a `todasLasTareas.html` (con filtros)
5. **Crear tarea**: Navega a `crearTarea.html` → Llena formulario
6. **Cerrar sesión**: Click en "Tancar Sessió" → Vuelve a login

---

## Limitaciones Actuales

### 1. Datos Hardcodeados

Las tareas mostradas en `index.html` y `todasLasTareas.html` están escritas directamente en el HTML, no se cargan dinámicamente desde localStorage.

**Ejemplo**:
```html
<!-- Esto debería ser generado por JavaScript -->
<article>
    <h3>Finaliza el componente de React</h3>
    <p>Construye un componente rehusable</p>
</article>
```

**Solución pendiente**: Crear funciones JS que lean de localStorage y generen el HTML dinámicamente.

### 2. Filtros No Funcionales

Los filtros en `todasLasTareas.html` son solo UI, no filtran nada.

**Pendiente**: Implementar lógica de filtrado en JavaScript que:
- Escuche clicks en opciones de filtro
- Filtre el array de tareas
- Re-renderice la lista

### 3. Búsqueda No Implementada

La barra de búsqueda es decorativa.

**Pendiente**: Implementar búsqueda en tiempo real que filtre por:
- Título
- Descripción
- Tags

### 4. Formulario de Crear Tarea No Conectado

El formulario en `crearTarea.html` no tiene event handlers.

**Pendiente**: Agregar `onsubmit` que:
1. Recopile datos del formulario
2. Llame a `crearTarea()`
3. Redirija a `index.html` o `todasLasTareas.html`

### 5. Sin Validación de Formularios

Los inputs no validan datos.

**Pendiente**: Agregar validaciones:
- Campos obligatorios
- Formato de fecha
- Longitud de texto

### 6. localStorage No Escalable

Usar localStorage para almacenar tareas es temporal.

**Pendiente**: Migrar a:
- Base de datos (MySQL, PostgreSQL, MongoDB)
- API REST o GraphQL
- Autenticación real con JWT

### 7. Sin Editar/Eliminar Tareas

No hay UI ni lógica para modificar o borrar tareas.

**Pendiente**: Agregar botones de edición/eliminación en cada tarjeta.

### 8. Sin Responsive Design

El diseño está optimizado para desktop (1440px).

**Pendiente**: Agregar media queries y layouts responsivos para móvil/tablet.

---

## Roadmap Futuro

### Fase 1: Funcionalidad Básica (Corto Plazo)
- [ ] Conectar formulario de crear tarea con localStorage
- [ ] Renderizado dinámico de tareas desde localStorage
- [ ] Implementar filtros funcionales
- [ ] Implementar búsqueda en tiempo real
- [ ] Agregar validación de formularios

### Fase 2: CRUD Completo (Medio Plazo)
- [ ] Función de editar tarea
- [ ] Función de eliminar tarea
- [ ] Marcar tarea como completada
- [ ] Cambiar estado de tarea (pendiente → en progreso → completado)

### Fase 3: Backend y Base de Datos (Largo Plazo)
- [ ] Diseñar esquema de base de datos
- [ ] Crear API REST con Node.js/Express
- [ ] Autenticación con JWT
- [ ] Migrar datos de localStorage a base de datos
- [ ] Agregar roles de usuario (estudiante/profesor)

### Fase 4: Mejoras UX/UI (Largo Plazo)
- [ ] Diseño responsive completo
- [ ] Animaciones y transiciones
- [ ] Drag & drop para reordenar tareas
- [ ] Notificaciones de tareas próximas a vencer
- [ ] Modo oscuro

### Fase 5: Features Avanzadas (Futuro)
- [ ] Colaboración en tareas (múltiples usuarios)
- [ ] Comentarios en tareas
- [ ] Adjuntar archivos
- [ ] Calendario de tareas
- [ ] Exportar a PDF
- [ ] Integración con Google Calendar

---

## Notas para Desarrolladores

### Convenciones de Código

1. **Nombres de archivos**: camelCase (ej: `todasLasTareas.html`, `crearTarea.html`)
2. **Nombres de clases CSS**: Tailwind utilities (no CSS custom)
3. **Nombres de variables TypeScript**: camelCase (ej: `usuariActual`, `novaTarea`)
4. **Nombres de funciones**: camelCase (ej: `crearTarea()`, `tancarSesio()`)

### Clases Tailwind Más Usadas

```css
/* Layout */
.flex, .flex-col, .grid, .grid-cols-3

/* Sizing */
.w-[335px], .h-[66px], .w-full, .h-full

/* Spacing */
.gap-4, .gap-[17px], .p-4, .px-4, .py-2

/* Colors */
.bg-primary, .bg-neutral-light, .text-primary-dark, .border-primary-dark

/* Typography */
.text-base, .text-2xl, .font-bold, .font-semibold, .font-extrabold

/* Borders */
.border-2, .rounded, .rounded-lg

/* Effects */
.hover:bg-gray-50, .transition-colors, .focus:ring-2
```

### Estructura de Página Típica

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <!-- CDNs: Tailwind, Google Fonts, Font Awesome -->
    <!-- Tailwind config inline -->
    <!-- Script de sesión (si es página protegida) -->
    <script src="./dist/script.js" defer></script>
</head>
<body class="bg-white font-sans min-h-screen p-6">
    <div class="flex gap-[17px] max-w-[1440px] mx-auto">
        <!-- Sidebar -->
        <aside class="w-[335px]">...</aside>
        
        <!-- Contenido principal -->
        <main class="flex-1">...</main>
    </div>
    
    <!-- Botón cerrar sesión -->
    <button onclick="tancarSesio()">Tancar Sessió</button>
</body>
</html>
```

---

## Debugging

### Problema: Redirect a login.html constante

**Causa**: `localStorage.getItem("usuariActual")` retorna `null`

**Solución**:
1. Abre DevTools → Application → Local Storage
2. Verifica que existe la key `usuariActual`
3. Si no existe, manualmente agrega: Key: `usuariActual`, Value: `test_user`

O usa la versión `-dev` de archivos que simulan sesión automáticamente.

### Problema: Estilos no se aplican

**Causa**: Tailwind config no carga correctamente

**Solución**:
1. Verifica que el CDN de Tailwind está cargando: `https://cdn.tailwindcss.com`
2. Verifica que el script inline de config está presente en `<head>`
3. Usa DevTools → Network para verificar carga de recursos

### Problema: TypeScript no compila

**Causa**: Error de sintaxis o `tsconfig.json` mal configurado

**Solución**:
```bash
# Ver errores específicos
npx tsc

# Verificar configuración
cat tsconfig.json
```

---

## Referencias y Recursos

### Diseño Original
- **Figma**: [TaskGener Design](https://www.figma.com/design/zAulmgBMEDtZdLUihnyfiM/TaskGener)
- Documentación interna: `DESIGN_IMPLEMENTATION.md`, `ICON_COLOR_GUIDE.md`

### Tecnologías
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Tutoriales Relacionados
- localStorage API: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- Form Handling: [MDN Forms](https://developer.mozilla.org/en-US/docs/Learn/Forms)

---

## Contacto y Contribución

**Proyecto**: Lumen  
**Institución**: Jaume Viladoms Centre Educatiu  
**Repositorio**: [github.com/vandalieu06/mangaer-tasks](https://github.com/vandalieu06/mangaer-tasks)  
**Branch actual**: `main`

### Cómo Contribuir
1. Fork el repositorio
2. Crea una rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

---

## 📄 Licencia

Este proyecto es propiedad de Jaume Viladoms Centre Educatiu y está destinado exclusivamente para uso educativo.

---

**Última actualización**: 12 de diciembre de 2025  
**Versión del documento**: 1.0  
**Estado del proyecto**: En desarrollo activo
