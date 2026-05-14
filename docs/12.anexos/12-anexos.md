# 12. Anexos

Los anexos recogen material complementario sin sobrecargar el cuerpo principal de la memoria. A continuación se detalla el estado de cada anexo propuesto y el contenido disponible.

---

## Anexo A. Capturas de la aplicación móvil

Las capturas de pantalla de la aplicación deben generarse desde el dispositivo o emulador. Los lugares marcados para insertar capturas son:

| Pantalla | Ruta en la app | Estado |
|----------|---------------|--------|
| Login | `app/login.tsx` | Pendiente de capturar |
| Home | `app/(tabs)/index.tsx` | Pendiente de capturar |
| Productos | `app/(tabs)/productos/index.tsx` | Pendiente de capturar |
| Detalle producto | `app/(tabs)/productos/[id].tsx` | Pendiente de capturar |
| Scan (modo foto) | `app/(tabs)/scan/index.tsx` | Pendiente de capturar |
| Detalle factura | `app/facturas/[id].tsx` | Pendiente de capturar |
| Stats | `app/stats.tsx` | Pendiente de capturar |
| Configuración | `app/(tabs)/config/index.tsx` | Pendiente de capturar |
| Perfil | `app/(tabs)/config/perfil.tsx` | Pendiente de capturar |
| Preferencias | `app/(tabs)/config/preferencias.tsx` | Pendiente de capturar |
| Notificaciones | `app/(tabs)/config/notificaciones.tsx` | Pendiente de capturar |
| Categorías | `app/(tabs)/config/categorias.tsx` | Pendiente de capturar |
| Datos | `app/(tabs)/config/datos.tsx` | Pendiente de capturar |
| Información | `app/(tabs)/config/informacion.tsx` | Pendiente de capturar |

### Guía para generar las capturas

1. **Iniciar la app** con `npm run start` y abrirla en un emulador de Android/iOS o dispositivo físico con Expo Go.
2. **Navegar a cada pantalla** indicada en la tabla anterior.
3. **Tomar captura** con las herramientas del sistema operativo (Android: botón de encendido + bajar volumen; iOS: botón lateral + subir volumen; emulador: icono de cámara en la barra de herramientas).
4. **Transferir las imágenes** al directorio `docs/assets/screenshots/` y nombrarlas según el patrón `screenshot-<pantalla>.png` (ej. `screenshot-login.png`, `screenshot-home.png`).
5. **Insertar en la memoria** sustituyendo los marcadores `Pendiente de insertar captura de pantalla` por la sintaxis estándar de Markdown: `![Descripción](../assets/screenshots/screenshot-<pantalla>.png)`. Si se usa un procesador de textos (Word, LibreOffice), insertar la imagen directamente.

> **Recomendación:** Utilizar el emulador de Android con resolución 1080×1920 píxeles para obtener capturas nítidas y uniformes. Asegurarse de que los datos de demostración estén visibles para que las pantallas no aparezcan vacías.

---

## Anexo B. Prototipos de Figma

Los diseños en Figma se encuentran en la carpeta `docs/figma/` del repositorio. Incluyen especificaciones para:

| Pantalla | Archivo SPEC | Estado |
|----------|-------------|--------|
| Home | `figma/01-home/SPEC.md` | Especificación completa |
| Categorías | `figma/00-categorias/SPEC.md` | Especificación completa |
| Configuración | `figma/02-configuracion/SPEC.md` | Especificación completa |
| Scan | `figma/03-escanear-facturas/SPEC.md` | Especificación completa |
| Productos | `figma/04-productos/SPEC.md` | Especificación completa |
| Sistema de diseño | `docs/DESIGN.md`, `docs/DESIGNLAYOUT.md` | Documentación de diseño en desarrollo |

Para insertar imágenes de los prototipos, exportar desde Figma y ubicarlas en una carpeta de assets del proyecto, por ejemplo `docs/assets/figma/`, cuando se cierre la fase de diseño.

---

## Anexo C. Diagramas del sistema

### Diagramas disponibles (contenido textual completo)

| Diagrama | Documento | Tipo |
|----------|-----------|------|
| Entidad-Relación (BD) | `04-diseno-aplicacion.md` §4.2.1 | Mermaid (código incrustado) |
| Diagrama de actores | `04-diseno-aplicacion.md` §4.1.1.1 | Mermaid |
| Diagrama de casos de uso | `04-diseno-aplicacion.md` §4.1.1.2 | Mermaid |
| Diagrama de arquitectura frontend | `04-diseno-aplicacion.md` §4.1.2 | Mermaid |
| Flujo inicio de sesión | `04-diseno-aplicacion.md` §4.1.2.1 | Mermaid sequenceDiagram |
| Flujo escaneo factura | `04-diseno-aplicacion.md` §4.1.2.1 | Mermaid sequenceDiagram |
| Flujo filtrado productos | `04-diseno-aplicacion.md` §4.1.2.1 | Mermaid sequenceDiagram |
| Diagrama de clases de diseño | `04-diseno-aplicacion.md` §4.1.2.2 | Mermaid classDiagram |
| Diagrama de estados de factura | `04-diseno-aplicacion.md` §4.1.2.3 | Mermaid stateDiagram |
| Mapa de navegación de la app | `04-diseno-aplicacion.md` §4.1.3 | Mermaid |
| Diagrama de arquitectura general | `02-planificacion-proyecto.md` §2.3 | Mermaid |
| Diagrama de comunicación frontend-backend | `09-documentacion-api.md` | Mermaid sequenceDiagram |
| Cronograma del proyecto | `02-planificacion-proyecto.md` §2.1 | Mermaid gantt |
| Organigrama de empresa | `03-empresa.md` §3.4 | Mermaid |

### Elementos visuales pendientes

No quedan diagramas técnicos pendientes en formato Mermaid. Los elementos visuales pendientes se limitan a capturas de pantalla, pósteres y exportaciones gráficas de Figma.

---

## Anexo D. Empresa y prevención

La información sobre la empresa y los pósteres de RSC, ODS y prevención de riesgos se desarrollan en el capítulo `03-empresa.md` de la memoria.

Pendiente de generar:
- [ ] Póster RSC y ODS
- [ ] Póster prevención de riesgos

---

## Anexo E. Verificación técnica

### Resultado de lint (app móvil)

```bash
> lumen@1.0.0 lint
> expo lint

app/(tabs)/scan/index.tsx        # warnings de imports y variables no usadas
src/components/ui/CategorySelect/CategorySelect.tsx  # warning de import no usado
src/hooks/useScanCamera.tsx      # warning de tipo importado no usado
```

**Resultado:** 0 errores, 8 warnings. Los warnings son de imports y variables no usadas; no bloquean la ejecución.

### Resultado de tests (servicio OCR)

```bash
> uv run pytest
============================= test session starts ==============================
collected 41 items

tests/test_llm_factory.py .....                                        [ 12%]
tests/test_ocr_service.py .....................                        [ 63%]
tests/test_producto.py .....                                           [ 75%]
tests/test_routes.py ..........                                        [100%]

============================== 40 passed, 1 xfailed ============================
```

**Resultado:** 40 tests pasan, 1 esperado como fallo (`xfail`) — bug conocido en validación de imagen vacía (`test_process_ticket_with_empty_data_handles_cv2_error`).

En la revisión final de la documentación no se ha podido reejecutar este comando porque `uv` no está instalado en el entorno y `python -m pytest` falla con `No module named pytest`. El resultado anterior se conserva como evidencia documentada del conjunto de tests, y la limitación de ejecución queda registrada.

### Resultado de build (landing page)

```bash
> lumen-landing@0.1.0 build
> astro build

1 page(s) built
build complete
```

**Resultado:** build estático completado correctamente.

### Resultado de verificación backend Go

```bash
go test ./...
```

**Resultado:** no ejecutado en esta revisión porque `go` no está disponible en el entorno (`go not found`).

### Observación de integración OCR

La verificación documental detecta una diferencia de contrato entre backend Go y OCR Flask:

- El OCR Flask devuelve un array de productos con campos `nombre`, `precio_total`, `cantidad` y `precio_unitario`.
- El backend Go intenta decodificar un objeto `OCRResponse` con `success`, `company`, `amount`, `description` y `products`.
- La app móvil todavía envía el archivo como `factura` a `/api/factura`, mientras que OCR espera `image` en `/api/process-ticket` y backend espera `image` dentro de `POST /api/transactions`.
- Tarea pendiente: hacer que la app reciba los campos normalizados de la factura ya procesada desde backend, en lugar de mostrar estados simulados desde memoria local.

Esta diferencia no invalida los módulos por separado, pero sí queda como pendiente técnico para cerrar el flujo completo app-backend-OCR.

### Pruebas pendientes de ejecutar

- [ ] Pruebas de usabilidad (sesiones con usuarios)
- [ ] Revisión de accesibilidad (lector de pantalla, contraste, áreas táctiles)
- [ ] Pruebas unitarias en app móvil
- [ ] Pruebas unitarias en backend Go
- [ ] Pruebas de integración frontend-backend
- [ ] Prueba de integración app móvil → backend Go → OCR con contrato unificado

---

## Anexo F. Documentación backend

### Esquema de base de datos

El diagrama entidad-relación y el esquema lógico normalizado se encuentran en `04-diseno-aplicacion.md` §4.2. Las tablas se generan automáticamente mediante GORM `AutoMigrate` a partir de los modelos en `api/internal/domain/entities/models.go`.

### Endpoints de la API

La documentación completa de los endpoints del backend Go y del servicio OCR se encuentra en `09-documentacion-api.md`. Incluye:

- Backend Go (puerto 8080): 18 endpoints (auth, transacciones, categorías, tags, balance)
- Servicio OCR (puerto 3000): 3 endpoints (health, process-ticket, extract-text)
- Flujo de facturas con OCR: multipart, proxy, almacenamiento
- Autenticación Firebase y token de prueba

### Manual de instalación

El manual completo de instalación de todos los componentes (app móvil, backend Go, OCR, landing page, base de datos) se encuentra en `07-manual-instalacion-configuracion.md`.

### Variables de entorno

| Componente | Archivo | Variables |
|------------|---------|-----------|
| Backend Go | `api/.env` | `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`, `FIREBASE_CREDENTIALS`, `OCR_API_URL`, `OCR_API_TIMEOUT`, `UPLOAD_DIR` |
| OCR | `ocr-processor/.env` | `LLM_PROVIDER`, `OLLAMA_URL`, `OLLAMA_MODEL`, `OPENROUTER_KEY`, `OPENROUTER_URL_API`, `OPENROUTER_MODEL` |
| App móvil | — | `EXPO_PUBLIC_API_BASE_URL` (variable de entorno Expo) |

### Estructura del proyecto

| Componente | Ruta (relativa al raíz) | Tecnología |
|------------|--------------------------|------------|
| App móvil | `mobile-app/` | Expo + React Native |
| Backend Go | `api-main/api/` | Go + Chi + GORM |
| OCR | `ocr-processor/` | Python + Flask + PaddleOCR |
| Landing page | `landing-page/landing/` | Astro + Tailwind |
| Base de datos | `api-main/database/` | Docker Compose (PostgreSQL 17 + Redis 8.6) |

---

## Resumen de anexos completados y pendientes

| Anexo | Estado |
|-------|--------|
| A. Capturas de la app móvil | Pendiente de generar imágenes |
| B. Prototipos Figma | Especificaciones listas, pendiente exportar imágenes |
| C. Diagramas del sistema | Diagramas técnicos completados en Mermaid |
| D. Empresa y prevención | Contenido en `03-empresa.md`; pósteres pendientes |
| E. Verificación técnica | Lint y tests documentados; tablas de pruebas pendientes |
| F. Documentación backend | **Completo** (API, instalación, BD, variables de entorno, repositorios) |
