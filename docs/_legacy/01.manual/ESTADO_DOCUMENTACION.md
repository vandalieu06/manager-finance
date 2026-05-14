# Estado de la Documentación del Proyecto

## Resumen General

| Sección | Estado |
|---------|--------|
| 1. Definición del proyecto | ✅ Completado |
| 2. Planificación del proyecto | ✅ Completado |
| 3. Empresa | ⚠️ Parcialmente completo |
| 4. Diseño aplicación/página web | ⚠️ Parcialmente completo |
| 5. Desarrollo aplicación/página web | ⚠️ Parcialmente completo |
| 6. Pruebas | ⚠️ Parcialmente completo |
| 7. Manual de instalación y configuración | ⚠️ Parcialmente completo |
| 8. Guía de usuario | ⚠️ Parcialmente completo |
| 9. Documentación (ApiDoc) | ❌ Pendiente de backend |
| 10. Conclusiones | ⚠️ Revisión necesaria |
| 11. Bibliografía, webgrafía y otros recursos | ⚠️ Parcialmente completo |
| 12. Anexos | ❌ Pendiente |

---

## Detalle por Sección

### ✅ 1. Definición del proyecto

| Subapartado | Estado |
|-------------|--------|
| 1.1. Introducción | ✅ Completado |
| 1.1.1. Explicación de qué trata | ✅ Completado |
| 1.1.2. Propósito y objetivos que se quieren alcanzar | ✅ Completado |

**Archivo:** `01.manual/1. Definición proyecto.md`

---

### ✅ 2. Planificación del proyecto

| Subapartado | Estado |
|-------------|--------|
| 2.1. Temporización del proyecto | ✅ Completado |
| 2.2. Recursos y materiales | ✅ Completado |
| 2.3. Tecnologías escolhidas para llevar a cabo el desarrollo | ✅ Completado |

**Archivo:** `01.manual/2. Planificació del projecte.md`

---

### ⚠️ 3. Empresa: constitución, trámites y procesos iniciales

| Subapartado | Estado | Notas |
|-------------|--------|-------|
| 3.1. Descripción detallada de la empresa. Rasgos diferenciales | ✅ Completado | |
| 3.2. Forma Jurídica y trámites de constitución | ✅ Completado | |
| 3.3. RSC y ODS propuestos. Póster | ⚠️ Parcial |falta el póster |
| 3.4. Organigrama y reparto de tareas | ✅ Completado | Incluído organigrama Mermaid |
| 3.5. Convenio colectivo y contratación | ✅ Completado | |
| 3.6. Estudio de riesgos y Plan de prevención. Póster | ⚠️ Parcial |falta el póster |

**Archivo:** `01.manual/3. Empresa.md`

---

### ⚠️ 4. Diseño aplicación/página web

| Subapartado | Estado | Notas |
|-------------|--------|-------|
| 4.1. Especificación Funcional del Sistema | ⚠️ Parcial | Actualizada desde la app móvil en `Memoria_TFG_Textos_Actualizados.md` |
| 4.1.1. Especificación del sistema propuesto | ⚠️ Parcial | Verificada contra Expo/React Native; backend pendiente |
| 4.1.1.1. Descripción de los actores | ✅ Completado | Usuario, Firebase Auth, servicio local de facturas y envío HTTP de factura |
| 4.1.1.2. Modelo de casos de uso | ⚠️ Parcial | Casos implementados y previstos separados; incluye cámara, envío de factura y logout |
| 4.1.2. Diseño del sistema | ⚠️ Parcial | Falta completar con backend real |
| 4.1.2.1. Diagramas de secuencia | ❌ Pendiente | |
| 4.1.2.2. Diagrama de clases de diseño | ❌ Pendiente | |
| 4.1.2.3. Diagramas de estado | ❌ Pendiente | |
| 4.1.3. Interfaces de usuario: Mapa de formularios | ⚠️ Parcial | Mapa de pantallas móvil documentado |
| 4.2. Bases de datos* | ⚠️ Parcial | Entidades detectadas desde frontend; modelo real pendiente de backend |
| 4.2.1. Qué información se desea almacenar | ⚠️ Parcial | Producto, factura, campo detectado, producto de factura y notificación |
| 4.2.2. Modelo E/R | ❌ Pendiente | Requiere revisar backend |
| 4.2.3. Esquema lógico normalizado | ❌ Pendiente | Requiere revisar backend |
| 4.3. Diseño de la interfaz web | ⚠️ Parcial | Redactado como diseño de app móvil |
| 4.3.1. Prototipado | ⚠️ Parcial | Pendiente incorporar capturas de Figma |
| 4.3.2. Guía de estilo | ⚠️ Parcial | Paleta, tipografía y principios visuales documentados |

**Archivos:** 
- `01.manual/4. Diseño.md` (concepto de marca y sistema visual)
- `01.manual/Memoria_TFG_Textos_Actualizados.md` (textos verificados desde la app móvil)
- `03.dev/03-Arquitectura/01-EspecificacionTecnica.md` (contiene un modelo E/R de ejemplo)

---

### ⚠️ 5. Desarrollo aplicación/página web

| Subapartado | Estado |
|-------------|--------|
| 5.1. Elementos gráficos y multimedia | ✅ Completado |
| 5.2. Área clientes | ⚠️ Parcial |
| 5.3. Área administración | ❌ No implementado en app móvil |

**Notas:** La app móvil implementa el área de cliente con datos demo, captura real con cámara, envío HTTP de factura y servicios locales en memoria para la revisión. El área de administración no aparece en el frontend revisado.

---

### ⚠️ 6. Pruebas

| Subapartado | Estado |
|-------------|--------|
| 6.1. Pruebas de usabilidad | ❌ Pendiente |
| 6.2. Pruebas de accesibilidad | ⚠️ Parcial |
| 6.3. Pruebas (unitarias, de integración y de sistema) | ⚠️ Parcial |

**Notas:** El código contiene algunas etiquetas de accesibilidad y existe `npm run lint`. La revisión actual devuelve 0 errores y 8 warnings. No se han localizado pruebas automatizadas.

---

### ⚠️ 7. Manual de instalación y configuración

| Estado |
|--------|
| ⚠️ Parcial |

**Notas:** Instalación y ejecución de app móvil documentadas. Backend pendiente.

---

### ⚠️ 8. Guía de usuario

| Estado |
|--------|
| ⚠️ Parcial |

**Notas:** Guía de uso de pantallas móviles redactada en `Memoria_TFG_Textos_Actualizados.md`.

---

### ❌ 9. Documentación (ApiDoc)

| Estado |
|--------|
| ❌ Pendiente de backend |

**Notas:** En la app móvil se ha verificado envío HTTP de factura a `/api/factura` desde el flujo de cámara y una utilidad `authenticatedFetch` preparada para API protegida con Firebase. Productos, stats y revisión de facturas siguen sin consumir API propia.

---

### ⚠️ 10. Conclusiones

| Subapartado | Estado |
|-------------|--------|
| 10.1. Propósitos y objetivos alcanzados | ⚠️ Revisión necesaria |
| 10.2. Problemas y dificultades | ⚠️ Revisión necesaria |
| 10.3. Opinión personal y comentarios | ⚠️ Revisión necesaria |

**Archivo:** `01.manual/10. Conclusiones.md`

**Notas:** El archivo actual afirma objetivos como backend, OCR, IA, base de datos y Stripe como ya integrados. Conviene sustituir o matizar con las conclusiones ajustadas de `Memoria_TFG_Textos_Actualizados.md` hasta revisar backend.

---

### ⚠️ 11. Bibliografía, webgrafía y otros recursos

| Estado | Notas |
|--------|-------|
| ⚠️ Parcialmente completo | Falta completar con más referencias |

**Archivo:** `01.manual/11. Bibliografía, webgrafía i otros recursos..md`

---

### ❌ 12. Anexos

| Estado |
|--------|
| ❌ Pendiente |

---

## Tareas Pendientes Prioritarias

1. **Revisar backend para completar lo no verificable desde la app móvil**
   - API real y endpoints
   - Modelos de base de datos
   - OCR/IA productivo
   - Despliegue y configuración del servidor

2. **Completar sección 4 (Diseño)**
   - Diagramas de secuencia, clases y estado actualizados
   - Modelo E/R definitivo
   - Esquema lógico normalizado
   - Capturas o enlaces de prototipo Figma

3. **Completar sección 5 (Desarrollo)**
   - Integrar los textos móviles ya redactados
   - Decidir si existe o no área de administración en el alcance final

4. **Completar sección 6 (Pruebas)**
   - Ejecutar y documentar `npm run lint`
   - Realizar pruebas de usabilidad
   - Documentar accesibilidad y añadir pruebas automatizadas si procede

5. **Actualizar sección 10 (Conclusiones)**
   - Sustituir afirmaciones no verificadas por objetivos parciales o pendientes

6. **Completar sección 11 (Bibliografía)**
   - Añadir referencias técnicas de Expo, React Native, Firebase, NativeWind y herramientas usadas

7. **Crear sección 12 (Anexos)**
   - Capturas, diagramas, estructura de carpetas y resultados de verificación

---

## Documentación de Desarrollo Existente (no integrada)

Existe documentación de desarrollo en la carpeta `03.dev/` que podría servir de base:

- `03.dev/01-Introduccion/01-Objetivos.md` - Objetivos del proyecto
- `03.dev/02-Diseno/01-Implementacion.md` - Guía de implementación
- `03.dev/02-Diseno/02-GuiaEstilos.md` - Guía de estilos
- `03.dev/03-Arquitectura/01-EspecificacionTecnica.md` - Especificación técnica
- `03.dev/CLEAN_ARCHITECTURE_GUIDE.md` - Guía de arquitectura limpia
