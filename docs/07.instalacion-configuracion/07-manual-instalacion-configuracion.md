# 7. Manual de instalación y configuración

Este manual describe la instalación, configuración y ejecución de todos los componentes del proyecto Lumen:

1. **App móvil** (Expo + React Native)
2. **Backend Go** (API financiera con PostgreSQL)
3. **Servicio OCR** (Python + Flask + PaddleOCR)
4. **Landing page** (Astro + Tailwind)
5. **Base de datos y servicios auxiliares**

---

## 7.1 App móvil

### Requisitos previos

- Node.js (versión 18 o superior)
- npm (incluido con Node.js)
- Expo Go (en dispositivo físico) o emulador Android / simulador iOS
- Git

### Instalación

```bash
cd /home/adri/dev/github/manager-finance-repos/mobile-app
npm install
```

### Ejecución en desarrollo

```bash
npm run start          # Inicia el servidor de desarrollo Expo
npm run android        # Abre en Android
npm run ios            # Abre en iOS
npm run web            # Abre en navegador web
```

### Comprobación de calidad

```bash
npm run lint
```

Resultado esperado:

```
> lumen@1.0.0 lint
> expo lint

8 warnings, 0 errors
```

El comando finaliza sin errores. Los warnings corresponden a imports y variables no usadas; se recomienda limpiarlos para la entrega.

### Configuración de Firebase

La aplicación inicializa Firebase desde `src/services/firebase.ts`. Actualmente la configuración está directamente en el código. Para entornos productivos debe gestionarse mediante la variable de entorno `EXPO_PUBLIC_FIREBASE_CONFIG` o un mecanismo equivalente.

### Configuración de API

El proyecto incluye `src/services/api.ts`, que define `authenticatedFetch`. Esta utilidad:

1. Lee la URL base de `EXPO_PUBLIC_API_BASE_URL`.
2. Obtiene el token de Firebase del usuario autenticado.
3. Lo añade como cabecera `Authorization: Bearer <token>`.
4. Realiza la petición HTTP.

**NOTA:** Actualmente las pantallas principales trabajan con datos de demostración local. `authenticatedFetch` está preparada para cuando se integre con el backend Go.

---

## 7.2 Backend Go (API Financiera)

### Requisitos previos

- Go 1.25 o superior
- Docker y Docker Compose (para PostgreSQL y Redis)
- Git

### Instalación

```bash
cd /home/adri/dev/github/manager-finance-repos/api-main/api
```

### Base de datos

Levantar PostgreSQL y Redis con Docker Compose:

```bash
cd /home/adri/dev/github/manager-finance-repos/api-main/database
docker compose up -d
```

Esto inicia dos contenedores:

| Servicio | Puerto | Imagen | Propósito |
|----------|--------|--------|-----------|
| PostgreSQL | `5432` | `postgres:17` | Base de datos principal |
| Redis | `6379` | `redis:8.6-alpine` | Caché (pendiente de uso en código) |

### Variables de entorno

Copiar la plantilla `api/.env.sample` a `api/.env` y ajustar los valores:

```bash
cp .env.sample .env
```

El archivo `.env` completo contiene las siguientes variables:

```env
# Base de datos
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=admin
DB_NAME=postgres
DB_PORT=5432

# Firebase Admin SDK
FIREBASE_CREDENTIALS=config/lumen-d1c2d-firebase-adminsdk-fbsvc-7039455887.json

# OCR (proxy desde Backend Go hacia servicio OCR Flask)
OCR_API_URL=http://localhost:3000
OCR_API_TIMEOUT=30

# Almacenamiento local de imágenes de facturas
UPLOAD_DIR=./uploads
```

> **⚠️ Seguridad:** El archivo `.env` contiene credenciales de base de datos y la ruta al JSON de Firebase Admin SDK. No debe incluirse en el control de versiones ni compartirse. El JSON con credenciales de servicio de Firebase (`config/lumen-*.json`) contiene información sensible y tampoco debe subirse a repositorios públicos. El proyecto incluye `.env.sample` como plantilla segura.

### Firebase Admin SDK

Para autenticación real (no solo token de prueba), se necesita un archivo JSON de credenciales de servicio de Firebase. Colocarlo en `config/` y ajustar `FIREBASE_CREDENTIALS` en `.env` para que apunte a él.

Para desarrollo local es posible usar el **token de prueba** `"test-admin-uid"` sin necesidad de Firebase real.

### Migraciones

Las migraciones se ejecutan automáticamente al iniciar el backend mediante `AutoMigrate` de GORM. No es necesario ejecutar migraciones manuales.

> **Nota:** El archivo `database/init.sql` fue eliminado. `AutoMigrate` de GORM es la única fuente de verdad para el esquema de base de datos.

Archivo de migraciones: `internal/infrastructure/database/migrations.go`
Modelos que se migran automáticamente:

- `User`
- `Category`
- `Tag`
- `Transaction`
- `Invoice`
- `Product`

### Ejecución

```bash
cd /home/adri/dev/github/manager-finance-repos/api-main/api
go run ./cmd/api/main.go
```

El servidor arranca en **`http://localhost:8080`**.

También está disponible un `Makefile` con comandos abreviados:

```bash
make api    # Compila y ejecuta el binario (go build + ./mi-api)
```

### Verificación

```bash
curl http://localhost:8080/
# Respuesta esperada: "API de Gestión de Finanzas Personales"

# Login de prueba:
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@admin.com","password":"admin1234"}'
# Respuesta esperada: {"token":"test-admin-uid","uid":"test-admin-uid"}
```

---

## 7.3 Servicio OCR

### Requisitos previos

- Python ≥ 3.10
- `uv` (gestor de proyectos Python rápido; instalar con `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Opcional: Ollama (para LLM local) o una API Key de OpenRouter

### Instalación

```bash
cd /home/adri/dev/github/manager-finance-repos/ocr-processor
uv sync
```

### Variables de entorno

Copiar la plantilla y ajustar según el proveedor LLM deseado:

```bash
cp sample.env .env
```

Valores disponibles:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `LLM_PROVIDER` | `ollama` | Proveedor LLM: `"ollama"` o `"openrouter"` |
| `OLLAMA_URL` | `http://localhost:11434` | URL del servicio Ollama |
| `OLLAMA_MODEL` | `llama3.1:8b` | Modelo de Ollama |
| `OPENROUTER_KEY` | (vacío) | API Key de OpenRouter |
| `OPENROUTER_URL_API` | `https://openrouter.ai/api/v1` | URL base de OpenRouter |
| `OPENROUTER_MODEL` | `tencent/hy3-preview:free` | Modelo de OpenRouter |

**Con Ollama (local):**

```bash
# Instalar Ollama: https://ollama.com
# Descargar el modelo:
ollama pull llama3.1:8b

# Configurar .env:
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:9b
```

**Con OpenRouter (cloud):**

```bash
# Obtener API Key en: https://openrouter.ai/keys
# Configurar .env:
LLM_PROVIDER=openrouter
OPENROUTER_KEY=sk-or-v1-tu-api-key-aqui
OPENROUTER_MODEL=tencent/hy3-preview:free
```

### Ejecución

```bash
uv run main.py
```

El servidor arranca en **`http://localhost:3000`**.

### Verificación

```bash
curl http://localhost:3000/api/health
# Respuesta esperada: {"status":"ok"}
```

### Pruebas

```bash
uv run pytest
```

El conjunto de pruebas incluye tests para:

- Rutas HTTP (`test_routes.py`)
- Servicio OCR (`test_ocr_service.py`)
- Factory de LLM (`test_llm_factory.py`)
- Modelo Producto (`test_producto.py`)

### Docker (alternativa)

El proyecto incluye un `Dockerfile` para construir una imagen:

```bash
docker build -t lumen-ocr .
docker run -p 3000:5000 lumen-ocr
```

> **⚠️ Nota:** El Dockerfile actual expone el puerto `5000` pero el entry point real es `main.py` (puerto `3000`). Se recomienda revisar el `CMD` del Dockerfile antes de usarlo en producción.

---

## 7.4 Landing Page

### Requisitos previos

- Node.js 18 o superior
- npm
- Usa **Tailwind CSS v4** y **Astro 6** como framework

### Componentes disponibles

| Componente | Ruta | Función |
|-----------|------|---------|
| `Navbar` | `components/landing/Navbar.astro` | Barra de navegación superior |
| `Button` | `components/ui/Button.astro` | Botón reutilizable |
| `MaterialIcon` | `components/ui/MaterialIcon.astro` | Icono Material con prop `icon` |
| `BaseLayout` | `layouts/BaseLayout.astro` | Layout base con Head + estilos |

El footer de la página principal enlaza a `/privacy` y `/terms` (rutas pendientes de implementar).

### Instalación

```bash
cd /home/adri/dev/github/manager-finance-repos/landing-page/landing
npm install
```

### Ejecución en desarrollo

```bash
npm run dev
```

El servidor de desarrollo de Astro arranca en **`http://localhost:4321`**.

### Build de producción

```bash
npm run build
```

Genera los archivos estáticos en la carpeta `dist/`.

### Previsualizar el build

```bash
npm run preview
```

### Configuración

El proyecto es completamente estático. La configuración del sitio se define en `astro.config.mjs`:

```js
import { defineConfig } from "astro/config";
export default defineConfig({
  site: "https://lumen.app",
});
```

Para desplegar, subir el contenido de `dist/` a cualquier hosting estático (Netlify, Vercel, Cloudflare Pages, GitHub Pages, S3, etc.).

---

## 7.5 Resumen de puertos y servicios

| Servicio | Tecnología | Puerto | Ruta de proyecto |
|----------|------------|--------|------------------|
| App móvil | Expo + React Native | — | `mobile-app/` |
| Backend Go | Go + Chi + GORM | `8080` | `api-main/api/` |
| OCR | Python + Flask + PaddleOCR | `3000` | `ocr-processor/` |
| Landing | Astro + Tailwind | `4321` (dev) | `landing-page/landing/` |
| PostgreSQL | Docker (postgres:17) | `5432` | `api-main/database/` |
| Redis | Docker (redis:8.6-alpine) | `6379` | `api-main/database/` |

---

## 7.6 Seguridad

1. **No incluir credenciales en el repositorio.** Los archivos `.env`, `config/*.json` con claves de Firebase, y cualquier secreto deben estar en `.gitignore`.
2. **Firebase Admin SDK:** El archivo JSON de credenciales de servicio contiene una clave privada. No debe compartirse ni exponerse en el frontend.
3. **Firebase en frontend:** La configuración de Firebase en la app móvil (apiKey, projectId, etc.) puede estar en el código porque no incluye secretos, pero se recomienda usar variables de entorno (`EXPO_PUBLIC_*`) para facilitar distintos entornos.
4. **Token de prueba del backend:** El token `"test-admin-uid"` permite desarrollo sin Firebase real, pero no debe usarse en producción.
5. **OCR sin autenticación:** El servicio OCR no requiere autenticación. Si se expone públicamente, debe añadirse autenticación o protegerse mediante el backend Go como proxy.

---

## 7.7 Orden de arranque recomendado

Para un inicio completo del sistema en local:

1. Base de datos: `docker compose up -d` (PostgreSQL + Redis)
2. Backend Go: `go run ./cmd/api/main.go` (puerto 8080)
3. OCR: `uv run main.py` (puerto 3000)
4. App móvil: `npm run start` (Expo)
5. Landing (opcional): `npm run dev` (puerto 4321)

---

## 7.8 Solución de problemas comunes

| Problema | Posible causa | Solución |
|----------|--------------|----------|
| Backend no conecta a BD | PostgreSQL no iniciado | Ejecutar `docker compose up -d` |
| OCR da error 500 al procesar | LLM no disponible | Verificar `OLLAMA_URL` o `OPENROUTER_KEY` |
| `uv sync` falla | Python < 3.10 | Actualizar Python o usar `pyenv` |
| App móvil no envía factura | OCR no corriendo o URL incorrecta | Verificar OCR en puerto 3000 y `EXPO_PUBLIC_API_BASE_URL` |
| `go run` no encuentra módulos | Go 1.25 no instalado | Verificar con `go version` |
