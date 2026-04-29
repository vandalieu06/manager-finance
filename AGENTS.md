# AGENTS.md

## Repo Shape
- Work from the relevant subdirectory; there is no root package manager or root test command.
- `frontend/lumen` is the active Expo Router app. Use `npm` because `package-lock.json` is committed.
- `backend/api` is a Go API module with its own `go.mod`.
- `backend/ocr_app` is a Flask OCR service packaged by `pyproject.toml` and also pinned in `requirements.txt`/`uv.lock`.
- `AGENT.md` exists but is empty; this file is the instruction source.

## Frontend: `frontend/lumen`
- Install/run from `frontend/lumen`: `npm install`, `npm run start`, `npm run android`, `npm run ios`, `npm run web`.
- Verification: `npm run lint`; there is no test script. For TypeScript-only checks use `npx tsc --noEmit` from `frontend/lumen`.
- Routing is file-based via Expo Router; entry is `app/_layout.tsx`, and `app/index.tsx` redirects to `./login`.
- Path alias `@/*` maps to `frontend/lumen/*` in `tsconfig.json`.
- NativeWind is wired through `babel.config.js`, `metro.config.js`, `global.css`, and `tailwind.config.js`; design tokens are loaded from `constants/colors.js`.
- Expo experiments enable `typedRoutes` and `reactCompiler`; avoid unnecessary `useMemo`/`useCallback` unless there is a real need.
- Keep the GUI muy simple; preserve the current compact mobile-first style rather than adding complex layouts.

## Go API: `backend/api`
- Run/verify from `backend/api`: `go test ./...`, `go build ./...`, or `go run ./cmd/api/main.go`.
- `make api` builds `./cmd/api/main.go` to `mi-api` and immediately runs it.
- The API listens on `:8080`; routes are wired in `cmd/api/main.go` with chi.
- Startup requires local Postgres at `localhost:5432` with `user=admin password=admin dbname=postgres sslmode=disable`; the DSN is hard-coded in `internal/infrastructure/database/database.go`.
- Migrations are GORM `AutoMigrate` on startup in `internal/infrastructure/database/migrations.go`.

## OCR Service: `backend/ocr_app`
- Run from `backend/ocr_app`: `python main.py`; Flask listens on `0.0.0.0:3000`.
- Install with `pip install -r requirements.txt` if using pip; dependencies include heavy OCR/ML packages (`easyocr`, `torch`, `opencv`).
- `.env` is loaded by `main.py`; LLM extraction reads `MODEL_AI`, `OPENROUTER_URL_API`, and `OPENROUTER_KEY` in `infrastructure/llm/ollama_adapter.py`.
- OCR uses CPU by default (`OCRConfig.usa_gpu = False`).
- Endpoints are registered under `/api`: `GET /api/health`, `POST /api/extract-text`, `POST /api/process-ticket`; image upload field name is `image`.

## Docs Notes
- `docs/03.dev` contains older Spanish product/design docs for “Lumen”; verify against executable config before trusting details.
- Some docs describe HTML/Tailwind web pages, but the current frontend is Expo/React Native.
