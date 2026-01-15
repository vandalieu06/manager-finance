# Planificación del Proyecto
## Gestor de Finanzas Personales

---

## Fases del proyecto

### Fase 1: Análisis del proyecto
En esta fase se definen las bases del sistema, las funcionalidades y las tecnologías a utilizar.

#### Análisis general de la aplicación
- Análisis del objetivo de la app
- Identificación de usuarios y necesidades
- Definición del alcance (qué incluye y qué no)

#### Esquema inicial de la base de datos
- Usuarios
- Movimientos (ingresos y gastos)
- Categorías
- Tags / Tipos de gasto
- Facturas / documentos asociados

#### Tecnologías y frameworks
- Aplicación móvil: React Native
- Aplicación web: React
- Backend: Go y Python
- Base de datos: por definir
- Diseño y prototipado: Figma

---

## Funcionalidades de la aplicación

### Funcionalidades básicas (MVP)

#### Autenticación de usuarios
- Registro de usuario
- Inicio de sesión
- Cierre de sesión
- Recuperación de contraseña

#### Movimientos (ingresos y gastos)
- Añadir movimiento
- Actualizar movimiento
- Eliminar movimiento
- Listar historial de movimientos
- Filtrar por fecha
- Filtrar por categoría
- Filtrar por tipo (ingreso / gasto)
- Búsqueda por texto

#### Categorías
- Añadir categoría
- Actualizar categoría
- Eliminar categoría
- Asignar categoría a movimientos

#### Resumen financiero
- Cálculo del balance total
- Totales por categoría
- Resumen mensual de ingresos y gastos

---

### Funcionalidades extra (opcionales)

#### Tags / tipos de gasto
- Añadir tag
- Actualizar tag
- Eliminar tag
- Asignar uno o varios tags a un movimiento

#### Gestión de facturas
- Subir factura (imagen o PDF)
- Asociar factura a un movimiento
- Clasificar factura por tipo de gasto
- OCR para lectura automática de datos (opcional)

#### Presupuestos
- Definir presupuesto mensual por categoría
- Aviso cuando se supera el presupuesto

#### Exportación de datos
- Exportar movimientos a CSV
- Exportar informes a PDF

---

## Consideraciones técnicas
- Validación de datos de entrada
- Seguridad en contraseñas (hash)
- Control de acceso por usuario
- Confirmaciones en acciones críticas (eliminar)
- Estados vacíos y mensajes de ayuda al usuario

---

## Resultado esperado
- Aplicación web funcional
- Aplicación móvil funcional
- Backend con API operativa
- Documentación básica del proyecto
