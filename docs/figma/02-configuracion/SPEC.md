# SPEC - Pantalla Configuración

## Descripción General
Pantalla de configuración y gestión de la cuenta del usuario. Permite modificar perfil, ajustar preferencias, acceder a ayuda y gestionar datos.

## Propósito
- Permitir al usuario gestionar su perfil y preferencias
- Proporcionar acceso a funcionalidades de exportación de datos
- Ofrecer soporte y ayuda
- Configurar aspectos de la aplicación

---

## Apartados de la Pantalla

### 1. Perfil de Usuario
**Ubicación**: Primera sección, más prominent

**Contenido:**
- **Avatar**: Imagen de perfil (circular) o iniciales
- **Nombre**: Nombre completo del usuario
- **Email**: Correo electrónico asociado
- **Editar**: Botón o icono para editar perfil

**Sub-pantalla: Editar Perfil**
- Campo: Nombre
- Campo: Email
- Campo: Contraseña (cambiar)
- Campo: Avatar (cambiar foto)
- Botón: Guardar cambios
- Botón: Cancelar

### 2. Ajustes Generales

#### 2.1 Preferencias
| Ajuste | Tipo | Opciones |
|--------|------|----------|
| Moneda | Selector | EUR, USD, GBP... |
| Idioma | Selector | Español, Inglés... |
| Tema | Toggle | Claro / Oscuro (si aplica) |

#### 2.2 Notificaciones
| Ajuste | Tipo | Descripción |
|--------|------|-------------|
| Notificaciones push | Toggle | Activar/desactivar |
| Recordatorios | Toggle | Recordar escanear |
| Resumen semanal | Toggle | Envío semanal de resumen |

#### 2.3 Categorías
- **Ver categorías**: Lista de categorías existentes
- **Añadir categoría**: Crear nueva categoría personalizada
- **Editar categoría**: Modificar nombre/color/icono
- **Eliminar categoría**: Borrar categoría (con confirmación)

### 3. Datos y Privacidad

#### 3.1 Gestión de Datos
| Función | Descripción |
|---------|-------------|
| Exportar datos | Descargar todos los datos (CSV/JSON) |
| Importar datos | Cargar datos desde archivo |
| Sincronizar | Sincronizar con nube (si hay cuenta premium) |

#### 3.2 Privacidad
| Función | Descripción |
|---------|-------------|
| Ver política de privacidad | PDF/Link a política |
| Ver términos y condiciones | PDF/Link a términos |
| Eliminar cuenta | Borrar cuenta y todos los datos |

**Sub-pantalla: Confirmar eliminación**
- Advertencia de acción irreversible
- Campo: Escribir "ELIMINAR" para confirmar
- Botón: Confirmar eliminación

### 4. Información de la App

| Item | Descripción |
|------|-------------|
| Versión | Número de versión actual (ej: v1.0.0) |
| Construido | Fecha de compilación |
| Licencias | Licencias de código abierto |
| Changelog | Historial de versiones |

### 5. Ayuda y Soporte

| Item | Descripción |
|------|-------------|
| FAQ | Preguntas frecuentes expandable |
| Tutorial | Guía de uso de la app |
| Contactar | Email de soporte |
| Feedback | Enviar feedback/Reportar problema |

**Sub-pantalla: FAQ**
- Lista de preguntas frecuentes
- Cada item expandible (accordion)
- Categorías: General, Scanner, Productos, Cuenta

---

## Componentes Específicos Requeridos

### Profile Card
```
┌─────────────────────────────┐
│  ┌────┐  Juan Pérez         │
│  │ 👤 │  juan@email.com     │
│  └────┘  [Editar perfil]    │
└─────────────────────────────┘
```

### Settings Item (Toggle)
```
┌─────────────────────────────┐
│ 🔔 Notificaciones      [○] │
└─────────────────────────────┘
```

### Settings Item (Selector)
```
┌─────────────────────────────┐
│ 💶 Moneda           [EUR ▼] │
└─────────────────────────────┘
```

### Settings Item (Acción)
```
┌─────────────────────────────┐
│ 📤 Exportar datos         > │
└─────────────────────────────┘
```

### Settings Section Header
```
┌─────────────────────────────┐
│ PERFIL                      │
├─────────────────────────────┤
│ ...items...                 │
└─────────────────────────────┘
```

### FAQ Item (Expandable)
```
┌─────────────────────────────┐
│ ¿Cómo escanear un ticket? + │
├─────────────────────────────┤
│ (expandido)                 │
│ Abre la sección Escanear   │
│ y selecciona cámara...     │
└─────────────────────────────┘
```

---

## Estados de la Pantalla

### Estado: Normal
Todos los ajustes visibles y accesibles.

### Estado: Logueado
Muestra datos de usuario, opciones de cuenta.

### Estado: No logueado (si aplica)
Muestra "Iniciar sesión" prominent, menos opciones.

### Estado: Loading
- Skeleton en ajustes
- Spinner en operaciones largas

### Estado: Editing
- Formularios de edición activos
- Campos editables

### Estado: Confirmación
- Modales de confirmación para acciones importantes
- Ejemplo: eliminar cuenta, cambiar contraseña

---

## Consideraciones de Diseño

### Neobrutalismo
- Bordes de 2px en secciones
- Sombras suaves
- Spacing generoso (16px+ entre items)
- Border radius 16px en cards

### Accesibilidad
- Tappable areas de 44px mínimo
- Contraste adecuado en texto
- Labels claros para cada ajuste

### Seguridad
- Confirmación para acciones destructivas
- Indicadores visuales de cambios guardados

---

## Flujo de Usuario

```
[Configuración]
│
├── Perfil
│   └── [Editar perfil] → Formulario → Guardar/Cancelar
│
├── Ajustes
│   ├── Preferencias (moneda, idioma, tema)
│   ├── Notificaciones (toggles)
│   └── Categorías → Gestión de categorías
│
├── Datos
│   ├── Exportar → [Selector formato] → Descarga
│   ├── Importar → [Selector archivo]
│   └── Eliminar cuenta → [Confirmación] → Modal warning
│
├── Información
│   └── Versión, términos, privacidad (vistas solo)
│
└── Ayuda
    ├── FAQ → [Preguntas expandibles]
    ├── Tutorial
    ├── Contactar → [Formulario email]
    └── Feedback
```

---

## Notas de Implementación React Native

- Usar `FlatList` para ajustes (mejor performance)
- SectionList para grouping
- Switch para toggles
- Modal para confirmaciones
- WebView para documentos externos (T&C, privacidad)
- Share API para exportar archivos

---

## Referencias

- Documentación técnica: `docs/03.dev/03-Arquitectura/01-EspecificacionTecnica.md`
- Modelo de datos usuario: Pendiente definir

---

*Especificación creada: 6 de Abril de 2026*
*Versión: 1.0*