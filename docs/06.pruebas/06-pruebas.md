# 6. Pruebas

Las pruebas del proyecto se distribuyen entre sus tres componentes principales. El estado actual es desigual:

| Componente | Tests automatizados | Comando |
|------------|-------------------|---------|
| App móvil (Expo) | No tiene | Solo `npm run lint` |
| Backend Go | No tiene | — |
| OCR (Python/Flask) | **Sí tiene** (41 tests: 40 pasan y 1 `xfail`) | `uv run pytest` |

Este capítulo documenta tanto las pruebas existentes como las propuestas para completar la cobertura.

---

## 6.1. Pruebas del servicio OCR

El servicio OCR es el único componente que dispone de un conjunto de pruebas automatizadas. Utiliza **pytest** con **pytest-mock** para simular dependencias externas (OCR, LLM) y probar la lógica de negocio de forma aislada.

### 6.1.1. Ejecución

```bash
cd ocr-processor/
uv run pytest
```

Salida esperada:

```bash
============================= test session started =============================
collected 41 items

tests/test_llm_factory.py .....                                        [ 12%]
tests/test_ocr_service.py .....................                        [ 63%]
tests/test_producto.py .....                                           [ 75%]
tests/test_routes.py ..........                                        [100%]

============================== 40 passed, 1 xfailed ============================
```

- **40 tests pasan** correctamente.
- **1 test esperado como fallo** (`xfail`): `test_process_ticket_with_empty_data_handles_cv2_error` — bug conocido donde `cv2.imdecode` se ejecuta antes del bloque `try-catch`.

En la verificación final de esta revisión no se ha podido repetir la ejecución porque el entorno local no tiene `uv` instalado y `python -m pytest` devuelve `No module named pytest`. Se mantiene el resultado documentado como referencia del estado de pruebas existente, pero queda anotada la limitación del entorno de ejecución usado para cerrar la memoria.

### 6.1.2. Cobertura

Para ejecutar con cobertura:

```bash
uv run pytest --cov --cov-report=term-missing
```

### 6.1.3. Tests de rutas HTTP (`test_routes.py` — 10 tests)

Verifican los endpoints del servicio Flask simulando el servicio OCR subyacente.

| Test | Tipo | Resultado |
|------|------|-----------|
| `test_health_returns_ok` | Humo | ✅ Pasa |
| `test_process_ticket_without_image_returns_400` | Validación | ✅ Pasa |
| `test_process_ticket_with_empty_data_handles_cv2_error` | Error edge case | ⚠️ `xfail` (bug conocido) |
| `test_process_ticket_success` | Funcional | ✅ Pasa |
| `test_process_ticket_service_exception_returns_500` | Error handling | ✅ Pasa |
| `test_extract_text_without_image_returns_500` | Validación | ✅ Pasa |
| `test_extract_text_success` | Funcional | ✅ Pasa |
| `test_extract_text_service_exception_returns_500` | Error handling | ✅ Pasa |
| `test_validate_image_missing_field_returns_false` | Validación | ✅ Pasa |
| `test_validate_image_invalid_data_raises_cv2_error` | Error edge case | ✅ Pasa |

### 6.1.4. Tests del servicio OCR (`test_ocr_service.py` — 21 tests)

Prueban la lógica interna de parseo de respuestas del LLM y extracción de productos.

| Test | Tipo | Resultado |
|------|------|-----------|
| `test_parse_float_valid_integer` | Parseo | ✅ Pasa |
| `test_parse_float_valid_float` | Parseo | ✅ Pasa |
| `test_parse_float_comma_separator` | Parseo | ✅ Pasa |
| `test_parse_float_none` | Borde | ✅ Pasa |
| `test_parse_float_empty_string` | Borde | ✅ Pasa |
| `test_parse_float_invalid_string` | Borde | ✅ Pasa |
| `test_parse_float_already_float` | Borde | ✅ Pasa |
| `test_parse_float_already_int` | Borde | ✅ Pasa |
| `test_parse_valid_json_array` | Parseo LLM | ✅ Pasa |
| `test_parse_json_with_markdown_fences` | Parseo LLM | ✅ Pasa |
| `test_parse_empty_response` | Borde | ✅ Pasa |
| `test_parse_invalid_json_object_instead_of_array` | Parseo LLM | ✅ Pasa |
| `test_parse_invalid_json` | Borde | ✅ Pasa |
| `test_parse_array_with_non_dict_items` | Parseo LLM | ✅ Pasa |
| `test_parse_product_without_required_fields` | Validación | ✅ Pasa |
| `test_parse_product_without_nombre_uses_default` | Default | ✅ Pasa |
| `test_parse_multiple_valid_products` | Funcional | ✅ Pasa |
| `test_parse_float_values_with_comma` | Parseo | ✅ Pasa |
| `test_extract_products_calls_llm` | Integración | ✅ Pasa |
| `test_extract_products_handles_llm_error` | Error handling | ✅ Pasa |
| `test_extract_products_returns_empty_on_invalid_response` | Borde | ✅ Pasa |

### 6.1.5. Tests del factory LLM (`test_llm_factory.py` — 5 tests)

Verifican la selección y caché del proveedor LLM según variable de entorno.

| Test | Resultado |
|------|-----------|
| `test_get_provider_returns_ollama_by_default` | ✅ Pasa |
| `test_get_provider_returns_openrouter_when_env_set` | ✅ Pasa |
| `test_get_provider_returns_ollama_when_explicitly_set` | ✅ Pasa |
| `test_get_provider_raises_for_unknown_provider` | ✅ Pasa |
| `test_get_provider_returns_cached_instance` | ✅ Pasa |

### 6.1.6. Tests del modelo Producto (`test_producto.py` — 5 tests)

Prueban la serialización del dataclass `Producto`.

| Test | Resultado |
|------|-----------|
| `test_to_dict_returns_all_fields` | ✅ Pasa |
| `test_to_dict_with_none_values` | ✅ Pasa |
| `test_to_dict_partial_values` | ✅ Pasa |
| `test_producto_instantiation_positional` | ✅ Pasa |
| `test_producto_instantiation_named` | ✅ Pasa |

### 6.1.7. Bug conocido

El test `test_process_ticket_with_empty_data_handles_cv2_error` está marcado como `xfail` porque `cv2.imdecode` se ejecuta antes del bloque `try-catch` en `routes.py:32`, lo que puede lanzar una excepción no manejada. Se recomienda reestructurar la validación de imagen para capturar este caso.

---

## 6.2. Pruebas de la app móvil

### 6.2.1. Lint

La app móvil dispone de lint mediante Expo:

```bash
npm run lint
```

Resultado obtenido:

```bash
> lumen@1.0.0 lint
> expo lint

app/(tabs)/scan/index.tsx
  warnings de imports y variables no usadas

src/components/ui/CategorySelect/CategorySelect.tsx
  warning de import no usado

src/hooks/useScanCamera.tsx
  warning de tipo importado no usado
```

El comando finaliza sin errores, pero muestra **8 warnings**. No bloquean la ejecución, aunque conviene corregirlos antes de cerrar la entrega final.

### 6.2.2. Pruebas automatizadas (pendientes)

No se han localizado pruebas unitarias o de integración en la app móvil. En una versión más completa del proyecto, se recomienda añadir pruebas para:

- Funciones de filtrado de productos.
- Formateo de precios y fechas.
- Servicio local de facturas (`src/services/facturas.ts`).
- Componentes reutilizables.
- Flujos de navegación principales.
- Validaciones de formularios.

### 6.2.3. Pruebas de usabilidad

Pruebas recomendadas para evaluar si el usuario entiende los flujos principales sin explicación externa:

- Iniciar sesión.
- Interpretar la pantalla Home.
- Buscar y filtrar productos.
- Abrir el detalle de un producto.
- Capturar una factura con la cámara y enviarla.
- Añadir manualmente un producto a una factura.
- Revisar, validar o denegar una factura.
- Cambiar idioma o moneda desde preferencias.

Pendiente de insertar tabla de resultados de pruebas de usabilidad cuando se realicen sesiones con usuarios.

Para cerrar esta sección en la memoria final, se recomienda realizar sesiones con usuarios y recoger observaciones como tiempo necesario para completar tareas, errores cometidos y dudas durante el uso.

**Plantilla para la tabla de resultados:**

| Tarea | Usuario 1 | Usuario 2 | Usuario 3 | Media |
|-------|-----------|-----------|-----------|-------|
| Iniciar sesión | | | | |
| Interpretar el resumen de Home | | | | |
| Buscar y filtrar productos | | | | |
| Capturar una factura con la cámara | | | | |
| Añadir producto manual a factura | | | | |
| Validar/denegar una factura | | | | |
| Cambiar idioma en preferencias | | | | |

> **Nota:** Los valores deben reflejar tiempo en segundos, número de errores o una valoración subjetiva (1-5). Incluir observaciones cualitativas de cada sesión.

### 6.2.4. Pruebas de accesibilidad

El código ya incorpora algunas propiedades de accesibilidad en elementos interactivos: `accessibilityRole`, `accessibilityLabel` y `accessibilityState` en botones, pestañas, switches y acciones principales.

Aspectos a comprobar:

- Contraste entre texto y fondo.
- Tamaño mínimo de áreas táctiles.
- Lectura correcta con lector de pantalla.
- Descripción clara de botones e iconos.
- Navegación coherente entre pantallas.
- Comprensión de estados activos, seleccionados o deshabilitados.

Pendiente de insertar tabla de revisión de accesibilidad tras la validación con lector de pantalla, contraste y áreas táctiles.

**Plantilla para la revisión de accesibilidad:**

| Aspecto | Criterio | Estado | Observaciones |
|---------|----------|--------|---------------|
| Contraste texto/fondo | Relación ≥ 4.5:1 (texto normal) | ⬜ Pendiente | |
| Áreas táctiles | Mínimo 44×44 pt | ⬜ Pendiente | |
| Lectura con screen reader | Todos los elementos interactivos son accesibles | ⬜ Pendiente | |
| Etiquetas de accesibilidad | `accessibilityLabel` presente en botones e iconos | ⬜ Pendiente | |
| Roles de accesibilidad | `accessibilityRole` correcto en cada elemento | ⬜ Pendiente | |
| Navegación por teclado | Orden lógico de tabulación | ⬜ Pendiente | |
| Estados visibles | Active, disabled, selected diferenciados visualmente | ⬜ Pendiente | |

> Se recomienda usar **TalkBack** (Android) o **VoiceOver** (iOS) para validar la navegación con lector de pantalla. La herramienta **Lighthouse** (web) o el **inspector de accesibilidad** de las herramientas de desarrollo pueden ayudar a verificar contraste y áreas táctiles.

---

## 6.3. Pruebas del Backend Go

No se han localizado pruebas automatizadas en el backend Go. Sería recomendable añadir:

- Tests unitarios para los casos de uso (transacciones, categorías, tags, balance).
- Tests de integración para los endpoints HTTP.
- Tests del middleware de autenticación Firebase (token real y token de prueba).
- Tests del OCR Client (con mock del servicio OCR).
- Tests del Storage Service.

Además de las pruebas automatizadas, conviene validar manualmente el arranque del backend con PostgreSQL y Firebase configurados. El backend inicializa Firebase Admin SDK con el fichero indicado en `FIREBASE_CREDENTIALS`; si esa variable o el JSON de credenciales no existen, el arranque falla antes de exponer la API.

En la verificación final de esta revisión tampoco se ha podido ejecutar `go test ./...` porque el binario `go` no está disponible en el entorno (`go not found`).

---

## 6.4. Resumen de cobertura actual

| Componente | Tests | Cobertura funcional |
|------------|-------|-------------------|
| App móvil | 0 tests automatizados | Solo lint estático |
| Backend Go | 0 tests | — |
| OCR - Rutas HTTP | 10 tests | Health, process-ticket, extract-text, validación imagen |
| OCR - Servicio | 21 tests | Parseo floats, parseo LLM, extracción productos |
| OCR - Factory LLM | 5 tests | Selección proveedor, singleton, caché |
| OCR - Modelo Producto | 5 tests | Serialización to_dict, construcción |
| **Total OCR** | **41 tests** | **40 pasan, 1 xfail** |

> Los tests de `test_ocr_service.py` cubren métodos privados (`_parse_float`, `_parse_llm_response`, `_extract_products`) que se prueban tanto directamente como a través de `process_ticket`.

Comprobaciones realizadas durante el cierre documental:

| Componente | Comando | Resultado |
|------------|---------|-----------|
| App móvil | `npm run lint` | Ejecutado correctamente; 0 errores y 8 warnings |
| Landing page | `npm run build` | Ejecutado correctamente; build estático completado |
| OCR | `uv run pytest` | No ejecutado; `uv` no está instalado |
| OCR | `python -m pytest` | No ejecutado; falta módulo `pytest` |
| Backend Go | `go test ./...` | No ejecutado; `go` no está disponible en PATH |
