# 10. Conclusiones

## 10.1. Propósitos y objetivos alcanzados

El desarrollo de Lumen ha permitido construir un sistema de gestión financiera personal en estado de prototipo avanzado. Se ha conseguido implementar una base completa de interfaz, navegación y flujos de usuario en la app móvil, además de documentar e integrar los módulos principales de backend, base de datos, OCR y landing page.

Entre los objetivos alcanzados destacan:

- Desarrollo de una aplicación móvil con Expo y React Native.
- Organización de la navegación mediante Expo Router.
- Implementación de una interfaz visual coherente con el concepto de marca.
- Creación de pantallas principales: login, home, productos, scan, estadísticas y configuración.
- Implementación de filtros y búsqueda en productos.
- Captura de facturas mediante `expo-camera`, previsualización y envío HTTP de la imagen.
- Revisión de facturas mediante datos locales en memoria y acciones de validar o denegar.
- Integración inicial con Firebase Auth para el login.
- Cierre de sesión integrado con Firebase Auth.
- Desarrollo de un backend Go con API REST para transacciones, categorías, tags, balance y autenticación.
- Definición de la base de datos relacional con PostgreSQL y GORM AutoMigrate.
- Integración backend con servicio OCR para procesamiento de facturas mediante imagen.
- Documentación del servicio OCR en Python/Flask con PaddleOCR y proveedor LLM.
- Desarrollo de una landing page en Astro para presentar el producto.
- Documentación final de instalación, API, diseño, pruebas y anexos.

El proyecto también ha permitido aplicar conocimientos de diseño de interfaces, estructuración de código, componentes reutilizables, planificación, arquitectura backend, integración de servicios externos y documentación técnica.

El resultado final no se limita a una pantalla aislada, sino que agrupa una solución distribuida en varios repositorios: app móvil, backend Go, servicio OCR y landing page. Esta separación ha permitido documentar responsabilidades técnicas diferentes y preparar una base ampliable, aunque todavía no exista una integración productiva completa entre todos los módulos.

## 10.2. Problemas y dificultades

Durante el desarrollo se han identificado varias dificultades.

En primer lugar, el proyecto combina varias áreas técnicas: frontend móvil, backend, base de datos, OCR, inteligencia artificial y diseño de interfaz. Esta amplitud obliga a dividir correctamente el alcance y diferenciar entre prototipo móvil, funcionalidad local y funcionalidad productiva.

En segundo lugar, algunas partes previstas inicialmente requieren una integración más estable para presentarse como funcionalidad productiva. Es el caso de la sincronización completa entre app móvil y backend, el ajuste del contrato final de envío de facturas y la sustitución de datos de demostración por datos persistidos.

También ha sido necesario ajustar la documentación para evitar presentar como definitivas funcionalidades que todavía funcionan con datos de demostración o estado local en memoria. Esta revisión ha sido importante para que la memoria refleje con precisión el estado real del proyecto y separe claramente implementación, limitaciones y mejoras futuras.

Otra dificultad relevante ha sido la integración OCR. El servicio Python devuelve productos extraídos desde una imagen, mientras que el backend Go espera un DTO más amplio para actualizar transacciones. Esta diferencia de contrato evidencia la importancia de definir interfaces compartidas antes de cerrar la integración entre servicios.

## 10.3. Opinión personal y comentarios

El proyecto ha sido una experiencia útil para aplicar conocimientos técnicos en un caso práctico. Ha permitido trabajar con tecnologías actuales de desarrollo móvil y entender la importancia de organizar bien un proyecto desde el punto de vista del código, la interfaz y la documentación.

Uno de los aprendizajes principales ha sido la necesidad de distinguir entre diseño, prototipo móvil, backend funcional y sistema productivo. La aplicación móvil permite validar la experiencia de usuario y la estructura de pantallas; el backend y el OCR aportan la base técnica para evolucionar hacia una versión persistente y automatizada.

También se ha comprobado que una documentación rigurosa no debe ocultar limitaciones. En este proyecto, indicar que ciertos datos son de demostración, que algunas acciones son locales o que faltan pruebas automatizadas en determinados módulos mejora la calidad de la memoria, porque permite evaluar el trabajo por lo que realmente implementa y por la claridad de su evolución futura.

## 10.4. Líneas de trabajo futuras

El proyecto presenta varias vías de evolución identificadas durante el desarrollo:

**Integración plena app-backend:** La aplicación móvil está preparada con `authenticatedFetch` y el backend Go expone todos los endpoints necesarios. Queda pendiente conectar ambas partes para sustituir los datos de demostración por datos persistidos en PostgreSQL.

**Unificación del contrato de facturas:** Actualmente la app móvil envía imágenes a `/api/factura` con el campo `factura`, mientras que el backend Go espera `POST /api/transactions` con el campo `image`. Es necesario alinear ambos extremos para que el flujo OCR funcione de forma completa.

**Tarea pendiente — recepción de campos OCR en la app:** Falta completar la devolución de los campos extraídos por OCR hacia la aplicación móvil. El objetivo es que, tras subir una factura, la app reciba productos, importes, comercio y estado de revisión desde backend, en lugar de depender de datos simulados en memoria.

**Normalización del DTO OCR:** El servicio OCR Flask devuelve un array de productos con campos `nombre`, `precio_total`, `cantidad` y `precio_unitario`, mientras que el backend Go espera un objeto `OCRResponse`. Es necesario acordar un formato único o añadir una capa de adaptación.

**Pruebas automatizadas:** Incorporar tests unitarios y de integración en la app móvil (React Native Testing Library) y en el backend Go (testify/httptest). El servicio OCR ya dispone de 41 tests y sirve como referencia.

**Despliegue continuo:** Configurar un pipeline CI/CD con GitHub Actions que ejecute tests, lint y despliegue automático en entornos de prueba y producción.

**Registro de usuarios:** Implementar el flujo completo de registro en la app móvil, actualmente solo disponible mediante Firebase Console. Integrar la creación de usuario en backend Go para sincronizar el perfil.

**Notificaciones push:** Conectar los interruptores de notificaciones de la app con un servicio real (Firebase Cloud Messaging) para enviar recordatorios y resúmenes.

**Exportación de datos:** Implementar la funcionalidad de exportación CSV/PDF y sincronización con servicios externos.

**Gestión de presupuestos:** Añadir la posibilidad de definir presupuestos mensuales por categoría y mostrar alertas cuando se superen.

**Persistencia local offline:** Incorporar una base de datos local (SQLite con expo-sqlite) que permita a la app funcionar sin conexión y sincronizar cuando haya red.

La base desarrollada en este proyecto proporciona un punto de partida sólido y modular para continuar cualquiera de estas líneas de evolución.
