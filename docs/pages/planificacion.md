# Planificación del Proyecto

## Gestor de Finanzas Personales Multiplataforma

---

## Fases del proyecto

### Fase 1: Análisis y definición (1 semana)

- Análisis del problema y objetivos del proyecto
- Definición del alcance (funcionalidades incluidas y excluidas)
- Identificación de usuarios y casos de uso principales
- Definición de la arquitectura general (frontend + backend + base de datos)
- Elección de tecnologías y frameworks

---

## Backend

### Fase 2: Base de Datos (2 semanas)

#### Diseño de la base de datos

- Definición de entidades principales:
  - Usuarios
  - Movimientos (ingresos y gastos)
  - Categorías
  - Tags / tipos de gasto
  - Facturas / documentos
- Diseño del modelo entidad-relación (E/R)
- Normalización de la base de datos

#### Implementación

- Creación de la base de datos
- Aplicación del modelo físico
- Migración y gestión del esquema mediante ORM
- Definición de relaciones entre entidades

#### Seguridad de datos

- Protección de datos sensibles
- Restricciones de integridad
- Control de acceso por usuario

---

### Fase 3: API REST y lógica de negocio (2–3 semanas)

#### API REST

- Definición de endpoints REST
- Gestión de status codes HTTP correctos
- Validación de datos de entrada y salida
- Manejo de errores centralizado

#### Autenticación y seguridad

- Registro e inicio de sesión
- Hash y verificación de contraseñas
- Autenticación mediante JWT
- Protección de endpoints privados

#### ORM y lógica de negocio

- Definición de esquemas ORM
- Gestión de relaciones y transacciones
- Reglas de negocio (balances, cálculos, validaciones)

#### Gestión de archivos

- Conexión a almacenamiento S3 mediante MinIO
- Subida y recuperación de facturas (imagen / PDF)
- Asociación de archivos a movimientos

#### Procesamiento de imágenes

- Validación de formato y tamaño
- Almacenamiento seguro
- OCR opcional para lectura de datos (extra)

#### Infraestructura

- Definición de Docker Compose
- Servicios: backend, base de datos, MinIO
- Variables de entorno

#### Testing y documentación

- Tests básicos de la API
- Pruebas de endpoints
- Documentación de la API en Go (OpenAPI / Swagger o similar)

---

## Frontend

### Fase 4: Desarrollo Frontend Web (2 semanas)

- Desarrollo de la aplicación web
- Navegación entre pantallas
- Formularios con validación
- Gestión de estados (carga, error, vacío)
- Visualización de movimientos y resúmenes
- Diseño responsive

---

### Fase 5: Desarrollo Aplicación Móvil (2 semanas)

- Desarrollo de la app móvil con React Native
- Navegación entre pantallas
- Formularios de registro y movimientos
- Integración con la API REST
- Gestión de estados y errores
- Visualización de balances y estadísticas

---

## Diseño y Branding

### Fase 6: Diseño y experiencia de usuario (en paralelo)

#### Identidad visual

- Nombre del proyecto
- Diseño del logotipo
- Paleta de colores
- Tipografías
- Icono de la aplicación

#### Guía de estilo

- Uso del logotipo
- Colores principales y secundarios
- Tipografías y jerarquías
- Componentes UI básicos (botones, inputs, cards)

#### Prototipado

- Wireframes principales
- Prototipo navegable (Figma)
- Mockups de la app móvil y la web

---

## Material gráfico y comunicación

### Fase 7: Materiales finales

- Carteles promocionales (2)
- Mockups y capturas finales
- Vídeo promocional / demo del proyecto
- Guion o elevator pitch
- Presentación final (PPT o similar)

---

## Fase 8: Pruebas y cierre

- Pruebas funcionales
- Pruebas de usabilidad
- Corrección de errores
- Documentación final
- Preparación de la entrega
