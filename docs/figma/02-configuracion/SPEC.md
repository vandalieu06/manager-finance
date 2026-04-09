# SPEC - Pantalla Configuración

## Descripción General
Pantalla de configuración y gestión de la cuenta del usuario. Permite modificar perfil, ajustar preferencias, gestionar permisos del sistema, acceder a ayuda y gestionar datos.

## Propósito
- Permitir al usuario gestionar su perfil y preferencias
- Controlar permisos del sistema operativo (cámara, almacenamiento, notificaciones)
- Proporcionar acceso a funcionalidades de exportación de datos
- Ofrecer soporte y ayuda
- Configurar aspectos de la aplicación

---

## Apartados de la Pantalla

### Configuración de la App (config)

#### perfil
**Ubicación**: Primera sección, más prominente

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

---

#### preferencias
| Ajuste | Tipo | Opciones |
|--------|------|----------|
| Moneda | Selector | EUR, USD, GBP... |
| Idioma | Selector | Español, Inglés... |
| Tema | Toggle | Claro / Oscuro (si aplica) |

---

#### notificaciones
| Ajuste | Tipo | Descripción |
|--------|------|-------------|
| Notificaciones push | Toggle | Activar/desactivar |
| Recordatorios | Toggle | Recordar escanear |
| Resumen semanal | Toggle | Envío semanal de resumen |

---

#### categorías
- **Ver categorías**: Lista de categorías existentes
- **Añadir categoría**: Crear nueva categoría personalizada
- **Editar categoría**: Modificar nombre/color/icono
- **Eliminar categoría**: Borrar categoría (con confirmación)

---

#### Datos
| Función | Descripción |
|---------|-------------|
| Exportar datos | Descargar todos los datos (CSV/JSON) |
| Importar datos | Cargar datos desde archivo |
| Sincronizar | Sincronizar con nube (si hay cuenta premium) |

---

#### información
| Item | Descripción |
|------|-------------|
| Versión | Número de versión actual (ej: v1.0.0) |
| Construido | Fecha de compilación |
| Licencias | Licencias de código abierto |
| Changelog | Historial de versiones |

---

### Permisos de la app

Gestión de permisos nativos del dispositivo.

| Cámara | Acceso a la cámara del dispositivo | Escanear facturas/tickets |
| Almacenamiento | Acceso a fotos y archivos | Guardar/exportar datos |
| Notificaciones | Permiso de notificaciones nativas | Recibir notificaciones push |
| Ubicación (opcional) | Acceso a ubicación | Etiquetar gastos por ubicación |

#### Estados de permisos
| Estado | Indicador Visual | Descripción |
|--------|------------------|-------------|
| **Concedido** | ✓ Verde | Permiso activo |
| **Denegado** | ⚠️ Amarillo | Permiso denegado por el usuario |
| **Sin solicitar** | ○ Gris | Nunca se ha pedido el permiso |
| **Restringido** | 🔒 Gris | Restringido por el sistema (ej: menores) |

#### Interacción con permisos

Al hacer tap en un permiso:
- **Concedido**: Abrir configuración del sistema para gestionar
- **Denegado**: Mostrar modal con opción de "Abrir Settings" del sistema
- **Sin solicitar**: Solicitar permiso automáticamente (first request)

#### Diseño UI de Permisos

```
┌─────────────────────────────────────────────────┐
│ PERMISOS DEL SISTEMA                            │
├─────────────────────────────────────────────────┤
│ 📷 Cámara                    [✓ Concedido]     │
│    Necesario para escanear facturas             │
├─────────────────────────────────────────────────┤
│ 📁 Almacenamiento           [✓ Concedido]      │
│    Guardar y exportar tus datos                 │
├─────────────────────────────────────────────────┤
│ 🔔 Notificaciones            [⚠️ Denegado]     │
│    Activar para recibir alertas      [Activar] │
├─────────────────────────────────────────────────┤
│ 📍 Ubicación                 [○ No solicitado]  │
│    Etiquetar gastos por lugar         [Solicitar]│
└─────────────────────────────────────────────────┘
```

#### Flujo de solicitud de permisos

1. **Primera vez**: Solicitar permiso con explicación clara del uso
2. **Si denegado**: Mostrar banner/modal explicando por qué es necesario
3. **Permanentemente denegado**: Botón para abrir Settings del sistema

**Modal de explicación** (antes de solicitar):
```
┌─────────────────────────────────────────┐
│ 📷 Necesitamos acceso a tu cámara       │
├─────────────────────────────────────────┤
│ Para escanear tickets y extraer         │
│ automáticamente los productos de        │
│ tus compras.                            │
│                                         │
│ [Cancelar]          [Permitir]          │
└─────────────────────────────────────────┘
```

---

### Ayuda y Soporte

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

### Permission Item (Estados)
```
┌─────────────────────────────────────────┐
│ 📷 Cámara              [✓ Concedido]   │
│    Necesario para escanear facturas     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🔔 Notificaciones   [⚠️ Denegado]     │
│    Activar para recibir alertas [Activar]│
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📍 Ubicación       [○ No solicitado]   │
│    Etiquetar gastos por lugar   [Solicitar]│
└─────────────────────────────────────────┘
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

### Colores (Tokens Figma)
- Fondo: `base.white` (#FFFFFF)
- Texto: `base.black` (#000000)
- Bordes: `base.black` (#000000)
- Primary: `primary.v1` (#4ECDC4) - turquesa
- Éxito: `feedback.success.v1` (#22C55E)
- Error: `feedback.danger.v1` (#EF4444)
- Info: `feedback.info.v1` (#0EA5E9)

> ⚠️ Importante: Primary cambió de azul a turquesa (#4ECDC4)

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
├── Configuración de la App (config)
│   ├── perfil → Editar perfil → Formulario → Guardar/Cancelar
│   ├── preferencias (moneda, idioma, tema)
│   ├── notificaciones (toggles internos)
│   ├── categorías → Gestión de categorías
│   ├── Datos (exportar, importar, sincronizar)
│   └── información (versión, licencias)
│
├── Permisos del Sistema
│   ├── Cámara → Solicitar/Abrir Settings
│   ├── Almacenamiento → Solicitar/Abrir Settings
│   ├── Notificaciones → Solicitar/Abrir Settings
│   └── Ubicación (opcional) → Solicitar/Abrir Settings
│
└── Ayuda
    ├── FAQ → [Preguntas expandibles]
    ├── Tutorial
    ├── Contactar → [Formulario email]
    └── Feedback
```

---

## Notas de Implementación React Native / Expo

### Configuración General
- Usar `FlatList` para ajustes (mejor performance)
- SectionList para grouping
- Switch para toggles
- Modal para confirmaciones
- Share API para exportar archivos

### Gestión de Permisos

**Librerías recomendadas (Expo):**
- `expo-camera`: Permiso de cámara
- `expo-media-library`: Permiso de almacenamiento
- `expo-notifications`: Permiso de notificaciones
- `expo-location`: Permiso de ubicación

**Librerías recomendadas (React Native CLI):**
- `react-native-permissions`: Gestor unificado de permisos
- `react-native Linking` + `Settings`: Abrir Settings del sistema

**Ejemplo de flujo de verificación:**
```typescript
const checkPermission = async (permission: string) => {
  const status = await Permissions.getAsync(permission);
  return status.status; // 'granted' | 'denied' | 'undetermined'
};

const requestPermission = async (permission: string) => {
  const { status } = await Permissions.askAsync(permission);
  return status;
};

const openSettings = () => {
  Linking.openSettings();
};
```

**Patrón de UX para permisos:**
1. Verificar estado actual al entrar en pantalla
2. Si "undetermined", mostrar UI neutral con botón "Solicitar"
3. Si "denied", mostrar UI de advertencia con botón "Activar" → abrir Settings
4. Si "granted", mostrar UI de éxito con opción de gestionar

---

## Referencias

- Documentación técnica: `docs/03.dev/03-Arquitectura/01-EspecificacionTecnica.md`
- Modelo de datos usuario: Pendiente definir

---

*Especificación creada: 6 de Abril de 2026*
*Última actualización: 8 de Abril de 2026*
*Versión: 1.1*