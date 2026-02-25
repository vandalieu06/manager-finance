# Arquitectura OCR Service

## Visión General

Servicio REST Flask para procesamiento de tickets/facturas mediante OCR (EasyOCR) y LLM (Ollama).

## Estructura del Proyecto

```
ocr_app/
├── app/                      # Aplicación Flask
│   ├── __init__.py          # Factory de la app
│   ├── routes/
│   │   └── ticket.py        # Endpoints API
│   └── services/
│       └── ocr_service.py   # Orquestación OCR + LLM
├── core/                     # Núcleo de negocio
│   ├── entities/
│   │   └── producto.py      # Entidad Producto
│   └── ports/
│       ├── ocr_port.py      # Interfaz abstracta OCR
│       └── llm_port.py      # Interfaz abstracta LLM
├── infrastructure/           # Implementaciones concretas
│   ├── ocr/
│   │   └── easyocr_adapter.py  # Adaptador EasyOCR
│   └── llm/
│       └── ollama_adapter.py   # Adaptador Ollama
├── ocr/                     # Motor OCR original
│   ├── engine.py
│   └── preprocess.py
├── parser/                  # Parser original (sin uso actual)
├── config.py                # Configuración OCR
└── main.py                  # Entry point
```

## Flujo de Datos

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌────────────┐
│  Imagen     │────▶│  EasyOCR    │────▶│   Texto    │────▶│  Ollama   │
│  (JPEG/PNG) │     │  Adapter    │     │   OCR      │     │  Adapter   │
└─────────────┘     └──────────────┘     └─────────────┘     └────────────┘
                                                                    │
                                                                    ▼
                                                            ┌────────────┐
                                                            │   JSON     │
                                                            │ [productos]│
                                                            └────────────┘
```

## Componentes

### 1. Capa de Aplicación (`app/`)

**`app/__init__.py`** - Factory Flask
```python
def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(ticket_bp, url_prefix='/api')
    return app
```

**`app/routes/ticket.py`** - Endpoints
- `GET /api/health` - Verificación de salud
- `POST /api/process-ticket` - OCR + LLM → productos
- `POST /api/extract-text` - Solo OCR

**`app/services/ocr_service.py`** - Orquestador
```python
class OCRService:
    def process_ticket(self, image):
        # 1. Extraer texto OCR
        ocr_lines = self._ocr_adapter.extract_text(image)
        # 2. Unir líneas
        ocr_text = "\n".join(ocr_lines)
        # 3. Enviar a LLM
        productos = self._llm_adapter.extract_products(ocr_text)
        # 4. Retornar como dict
        return [p.to_dict() for p in productos]
```

### 2. Capa Core (`core/`)

Puertos (interfaces) que definen contratos:

**`ocr_port.py`**
```python
class OCRPort(ABC):
    @abstractmethod
    def extract_text(self, image) -> List[str]:
        pass
```

**`llm_port.py`**
```python
class LLMPort(ABC):
    @abstractmethod
    def extract_products(self, ocr_text: str) -> List[Producto]:
        pass
```

**`producto.py`**
```python
@dataclass
class Producto:
    nombre: str
    precio_total: Optional[float]
    cantidad: Optional[float]
    precio_unitario: Optional[float]
```

### 3. Capa Infrastructure (`infrastructure/`)

**`easyocr_adapter.py`** - Implementa `OCRPort`
- Usa el motor OCR original (`ocr/engine.py`)
- Inicialización lazy del motor

**`ollama_adapter.py`** - Implementa `LLMPort`
- Configurable: modelo (`llama3.2`) y URL (`http://localhost:11434`)
- Prompt optimizado para extraer productos de tickets
- Parseo de respuesta JSON

## Endpoints API

### GET /api/health
```bash
curl http://localhost:5000/api/health
```
Respuesta:
```json
{"status": "ok"}
```

### POST /api/extract-text
```bash
curl -X POST -F "image=@ticket.jpg" http://localhost:5000/api/extract-text
```
Respuesta:
```json
{"text": ["MERCADONA, S.A.", "A-46103834", ...]}
```

### POST /api/process-ticket
```bash
curl -X POST -F "image=@ticket.jpg" http://localhost:5000/api/process-ticket
```
Respuesta:
```json
[
  {"nombre": "Pan", "precio_total": 1.50, "cantidad": 1, "precio_unitario": 1.50},
  {"nombre": "Leche", "precio_total": 3.00, "cantidad": 2, "precio_unitario": 1.50}
]
```

## Configuración

### Ollama (`infrastructure/llm/ollama_adapter.py`)
```python
def __init__(self, 
    model_name: str = "llama3.2", 
    base_url: str = "http://localhost:11434"
):
```

### OCR (`config.py`)
```python
@dataclass(frozen=True)
class OCRConfig:
    ruta_imagen: str
    umbral_min_confianza: float = 0.25
    lenguajes_ocr: List[str] = ["es"]
    usa_gpu: bool = False
    # ... más parámetros de preprocesado
```

## Ejecución

```bash
# Activar entorno virtual
cd ocr_app
source .venv/bin/activate

# Ejecutar servidor
python main.py

# O con gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Requisitos

- Python 3.x
- Flask 3.1.3
- EasyOCR 1.7.2
- OpenCV
- Ollama corriendo en `localhost:11434`

## Notas

- El parser original (`parser/`) está obsoleto ahora que se usa LLM
- EasyOCR corre en CPU por defecto (más lento)
- Ollama debe estar instalado y con un modelo descargado (`llama3.2`)
