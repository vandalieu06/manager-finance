# Plan de Desarrollo - Lumen (React Native)

> **Objetivo**: Construir la app de gestión financiera paso a paso, aprendiendo React Native desde cero.  
> **Enfoque**: De hijos a padres (componentes simples → componentes complejos).  
> **Orden**: De más simple a más complejo.

---

## Fase 0: Fundamentos de React Native

### 0.1. Entorno y Configuración
- [ ] Comprender la estructura de un proyecto Expo (app/, components/, hooks/)
- [ ] Familiarizarse con `app.json` y configuración básica
- [ ] Ejecutar la app en emulator y ver los logs
- [ ] Entender la diferencia entre `View`, `Text`, `Pressable`

### 0.2. Estilos y Tailwind en RN
- [ ] Configurar Tailwind en el proyecto (`tailwind.config.js`)
- [ ] Entender cómo NativeWind traduce clases Tailwind a styles de RN
- [ ] Practicar con propiedades básicas: `flex`, `p-4`, `gap-2`
- [ ] Comprender el sistema de colores en Tailwind

**Meta Fase 0**: Poder renderizar una pantalla básica con View, Text y estilos.

---

## Fase 1: Componentes Atómicos (Building Blocks)

> ⚠️ **No puedes hacer un NavBar si no tienes un NavItem**  
> ⚠️ **No puedes hacer un Card si no tienes un Button**

### 1.1. Componentes de Texto y Visualización
- [ ] **Text basic**: Crear componente `Text` personalizado que use la fuente Inter
- [ ] **Heading**: Componente para títulos (H1, H2, H3)
- [ ] **Label**: Componente para labels de formularios

### 1.2. Componentes de Interacción
- [ ] **Button**: Botón primario con estados (default, pressed, disabled)
- [ ] **IconButton**: Botón circular con icono
- [ ] **Pressable**: Wrapper para elementos interactivos con feedback visual
- [ ] **TouchableOpacity**: Para elementos que necesitan feedback de opacidad

### 1.3. Componentes de Contenedor
- [ ] **Card**: Contenedor con borde, sombra y padding
- [ ] **Container**: Wrapper principal de pantalla con safeAreaView
- [ ] **Row/FlexRow**: Contenedor para elementos en fila
- [ ] **Column/FlexColumn**: Contenedor para elementos en columna

### 1.4. Componentes de Formulario
- [ ] **Input**: Campo de texto básico
- [ ] **TextArea**: Input multilínea
- [ ] **Select**: Selector dropdown
- [ ] **Checkbox**: Casilla de verificación (para filtros)

**Meta Fase 1**: Tener una librería de componentes reutilizables básicos.

---

## Fase 2: Sistema de Diseño (Colores, Tipografía, Espaciados)

> ⚠️ **No puedes hacer pantallas si no tienes el sistema de diseño definido**

### 2.1. Paleta de Colores
- [ ] Definir colores primarios en constants (primary, primary-dark)
- [ ] Definir colores neutros (neutral-light, neutral-medium, neutral-dark)
- [ ] Definir colores de estado (success, warning, error)
- [ ] Crear archivo `constants/colors.ts` exportando todos los colores

### 2.2. Tipografía
- [ ] Configurar fuente Inter en la app (expo-font)
- [ ] Definir escala tipográfica (text-xs, text-sm, text-base, text-lg, text-xl, text-2xl)
- [ ] Crear constantes para pesos de fuente (fontRegular, fontSemiBold, fontBold)
- [ ] Crear archivo `constants/typography.ts`

### 2.3. Espaciados y Dimensiones
- [ ] Definir tokens de espaciado (spacer-xs, spacer-s, spacer-m, spacer-l)
- [ ] Definir dimensiones comunes (buttonHeight, inputHeight, sidebarWidth)
- [ ] Definir constantes de border-radius
- [ ] Crear archivo `constants/spacing.ts`

### 2.4. Estilos Globales
- [ ] Configurar estilos globales en `global.css`
- [ ] Definir tema de Tailwind con los colores personalizados
- [ ] Verificar que los estilos se aplican correctamente

**Meta Fase 2**: Sistema de diseño consistente en toda la app.

---

## Fase 3: Navegación - De Componentes a Estructura

> ⚠️ **No puedes hacer un NavBar si no tienes un NavItem**  
> ⚠️ **No puedes hacer un TabBar si no tienes tabs individuales**

### 3.1. Navegación Individual (Building Blocks)
- [ ] **NavItem**: Elemento individual de navegación con icono y label
- [ ] **NavItemActive**: Variante activa del NavItem
- [ ] **Badge**: Notificación/count para elementos de nav

### 3.2. Contenedores de Navegación
- [ ] **Sidebar**: Barra lateral de navegación (versión web/desktop)
- [ ] **TabBar**: Barra de navegación inferior (versión móvil)
- [ ] **Header**: Barra superior de cada screen

### 3.3. Configuración de Navegación
- [ ] Instalar y configurar `@react-navigation/native`
- [ ] Configurar `@react-navigation/bottom-tabs` para navegación principal
- [ ] Configurar Stack Navigator para navegación entre pantallas
- [ ] Definir las rutas principales (Home, Settings, Scan, Products)

**Meta Fase 3**: Navegación funcional entre todas las pantallas principales.

---

## Fase 4: Estructura de Pantallas (Screens)

### 4.1. Pantalla de Login/Auth
- [ ] **LoginScreen**: Pantalla de inicio de sesión
  - [ ] Layout con logos (escuela + Lumen)
  - [ ] Input de usuario
  - [ ] Input de contraseña
  - [ ] Botón de entrada
  - [ ] Enlace a registro

### 4.2. Pantalla Home (Dashboard)
- [ ] **HomeScreen**: Dashboard principal
  - [ ] Header con título
  - [ ] Grid de estadísticas (tareas totales, en progreso, completadas)
  - [ ] Mini gráficos/visualizaciones
  - [ ] Sección de tareas recientes
  - [ ] Integración con navegación

### 4.3. Pantalla Settings (Configuración)
- [ ] **SettingsScreen**: Pantalla de configuración
  - [ ] Perfil de usuario (editar nombre, email)
  - [ ] Ajustes básicos de la app
  - [ ] Información de la app (versión, etc)
  - [ ] Sección de ayuda
  - [ ] Opción extraer datos

### 4.4. Pantalla de Escaneo (Scan)
- [ ] **ScanScreen**: Escaneo de facturas
  - [ ] Botones para tipo de subida (manual / foto)
  - [ ] Botón de historial de facturas
  - [ ] Vista previa de escaneo
  - [ ] Lista de facturas subidas

### 4.5. Pantalla de Productos
- [ ] **ProductsScreen**: Dashboard de productos
  - [ ] Lista de productos comprados
  - [ ] Filtros (por categoría, supermercado, fecha)
  - [ ] Rankings (productos más comprados)
  - [ ] División por supermercados

**Meta Fase 4**: Todas las pantallas principales implementadas.

---

## Fase 5: Estado y Datos (Gestión de Estado)

### 5.1. Estado Local (useState, useReducer)
- [ ] Entender `useState` para estado simple
- [ ] Entender `useReducer` para estado complejo
- [ ] Practicar con ejemplos: toggle, counter, form inputs

### 5.2. Estado Compartido (Context API)
- [ ] **AuthContext**: Gestionar estado de autenticación
- [ ] **UserContext**: Gestionar datos del usuario
- [ ] **TasksContext**: Gestionar lista de tareas/productos (si aplica)

### 5.3. Persistencia de Datos
- [ ] Configurar AsyncStorage para guardar datos localmente
- [ ] Implementar persistencia de sesión de usuario
- [ ] Implementar persistencia de datos de la app

**Meta Fase 5**: Poder gestionar y persistir datos en la app.

---

## Fase 6: Lógica de Negocio - Features Específicas

### 6.1. Sistema de Autenticación
- [ ] Validación de formulario de login
- [ ] Validación de formulario de registro
- [ ] Guardar sesión en AsyncStorage
- [ ] Cerrar sesión (logout)

### 6.2. Gestión de Tareas/Productos
- [ ] Crear nueva tarea/producto
- [ ] Editar tarea/producto existente
- [ ] Eliminar tarea/producto
- [ ] Marcar como completada

### 6.3. Sistema de Filtros
- [ ] Filtro por estado (pendiente/completado)
- [ ] Filtro por categoría
- [ ] Filtro por fecha
- [ ] Filtro por supermercado (para productos)
- [ ] Búsqueda por texto

### 6.4. Visualización de Datos
- [ ] Gráficos simples (pie chart, bar chart)
- [ ] Estadísticas en tiempo real
- [ ] Rankings de productos

**Meta Fase 6**: Features funcionales de la app.

---

## Fase 7: Integración de Cámara y Archivos

### 7.1. Escaneo de Facturas
- [ ] Integrar cámara para capturar fotos de facturas
- [ ] Subir archivos desde galería
- [ ] Preview de imagen escaneada
- [ ] Guardar referencia de factura

### 7.2. Historial de Facturas
- [ ] Lista de facturas subidas
- [ ] Ver detalles de cada factura
- [ ] Eliminar factura

**Meta Fase 7**: Funcionalidad de escaneo completa.

---

## Fase 8: Mejoras y Optimización

### 8.1. Experiencia de Usuario
- [ ] Loading states (spinners, skeleton screens)
- [ ] Error states (mensajes de error amigables)
- [ ] Empty states (cuando no hay datos)
- [ ] Pull-to-refresh

### 8.2. Animaciones
- [ ] Animaciones básicas con `react-native-reanimated`
- [ ] Transiciones entre pantallas
- [ ] Feedback visual en interacciones

### 8.3. Responsive Design
- [ ] Adaptar layout para diferentes tamaños de pantalla
- [ ] Optimizar para tablets

**Meta Fase 8**: App pulida y lista para producción.

---

## Resumen de Dependencias (Hijo → Padre)

```
Text → Heading → [Screen Headers]
     ↓
Button → IconButton → [Toolbar, ActionButtons]
     ↓
Card → [TaskCard, ProductCard, StatCard]
     ↓
Input → TextArea → [Form Fields]
     ↓
NavItem → NavBar/TabBar → [Navigation]
     ↓
Screen Layout → [HomeScreen, SettingsScreen, etc]
     ↓
App Navigator → [Navigation Structure]
```

---

## Orden Recomendado de Implementación

1. **Fase 0**: Configuración básica + Fundamentos
2. **Fase 1**: Componentes atómicos (Text, Button, Card, Input)
3. **Fase 2**: Sistema de diseño (colores, tipografía)
4. **Fase 3**: Navegación (NavItem → NavBar → Tab Navigator)
5. **Fase 4**: Estructura de pantallas (screens vacías primero)
6. **Fase 5**: Estado y datos (Context, AsyncStorage)
7. **Fase 6**: Lógica de negocio (CRUD, filtros)
8. **Fase 7**: Cámara y archivos
9. **Fase 8**: Mejoras finales

---

## Recursos para Aprender

- [Documentación oficial Expo](https://docs.expo.dev/)
- [React Native](https://reactnative.dev/docs/getting-started)
- [NativeWind](https://www.nativewind.dev/)
- [React Navigation](https://reactnavigation.org/docs/getting-started)

---

*Plan creado para ayudarte a aprender React Native paso a paso mientras construyes Lumen.*