# Guía: Clean Architecture en tu Proyecto de Finanzas

## 1. ¿Qué es Clean Architecture?

Clean Architecture es una forma de organizar el código en **capas concéntricas** donde las dependencias siempre apuntan **hacia el centro**:

```
         ┌─────────────────────────────────────┐
         │         Handlers (HTTP)             │  ← Capa externa
         └──────────────────┬──────────────────┘
                            │
         ┌──────────────────▼──────────────────┐
         │       Application (Use Cases)       │  ← Capa de lógica
         └──────────────────┬──────────────────┘
                            │
         ┌──────────────────▼──────────────────┐
         │      Domain (Entities, Interfaces)  │  ← Capa interna
         └─────────────────────────────────────┘
                            ▲
                            │
         ┌──────────────────┴──────────────────┐
         │      Infrastructure (DB, Auth)      │  ← Capa externa
         └─────────────────────────────────────┘
```

**Regla principal**: El dominio NO conoce a nadie. Todo lo demás depende del dominio.

---

## 2. Capas del Proyecto

### 📁 Domain (Capa más interna)

Aquí están las **entidades** y los **contratos** (interfaces). Esta capa no tiene dependencias externas.

**Archivos:**
- `internal/domain/entities/models.go` - Tus modelos de negocio
- `internal/domain/repositories/interfaces.go` - Contratos para acceder a datos
- `internal/domain/valueobjects/money.go` - Value objects

```go
// internal/domain/repositories/interfaces.go
type TransactionRepository interface {
    Create(transaction *entities.Transaction) error
    GetByID(id uint) (*entities.Transaction, error)
    GetAllByUserID(userID uint) ([]entities.Transaction, error)
    // ...
}
```

**¿Por qué interfaces aquí?** El dominio define QUÉ se puede hacer, no CÓMO se hace.

---

### 📁 Application (Capa de lógica de negocio)

Aquí están los **Use Cases** (casos de uso). Esta capa contiene la lógica de negocio pura.

**Archivos:**
- `internal/application/usecases/transaction/usecase.go`
- `internal/application/usecases/auth/usecase.go`
- `internal/application/dto/` - Objetos de transferencia de datos

```go
// internal/application/usecases/transaction/usecase.go
func (uc *UseCase) Create(userID uint, req dto.CreateTransactionRequest) (*dto.TransactionResponse, error) {
    // 1. Validar que la categoría existe
    category, err := uc.repo.GetCategoryByID(req.CategoryID)
    if err != nil {
        return nil, ErrCategoryNotFound
    }
    
    // 2. Crear la transacción
    transaction := &entities.Transaction{
        Type:        req.Type,
        Amount:      entities.Money(req.Amount),
        // ...
    }
    
    if err := uc.repo.CreateTransaction(transaction); err != nil {
        return nil, err
    }
    
    // 3. Retornar respuesta
    return &dto.TransactionResponse{...}, nil
}
```

**¿Qué hace un Use Case?** Orchestrar la lógica de negocio. En este caso:
1. Valida la categoría
2. Crea la entidad
3. Persiste usando el repository
4. Retorna el resultado

---

### 📁 Infrastructure (Capa externa)

Aquí están las **implementaciones concretas**: Base de datos, JWT, etc.

**Archivos:**
- `internal/infrastructure/database/repository.go` - Implementación GORM
- `internal/infrastructure/auth/jwt.go` - Generación/validación JWT
- `internal/infrastructure/auth/password.go` - Hash de contraseñas

```go
// internal/infrastructure/database/repository.go
func (r *Repository) CreateTransaction(transaction *entities.Transaction) error {
    return r.db.Create(transaction).Error
}
```

**¿Por qué está separado?** Puedes cambiar de GORM a otro ORM sin modificar la lógica de negocio.

---

### 📁 Handlers (Capa más externa)

Aquí están los **controladores HTTP** que reciben las peticiones.

**Archivos:**
- `internal/handlers/transaction.go`
- `internal/handlers/auth.go`

```go
// internal/handlers/transaction.go
func (h *TransactionHandler) Create(w http.ResponseWriter, r *http.Request) {
    // 1. Obtener usuario del contexto (del JWT)
    user := middleware.GetUserFromContext(r.Context())
    
    // 2. Decodificar el request JSON
    var req dto.CreateTransactionRequest
    json.NewDecoder(r.Body).Decode(&req)
    
    // 3. Llamar al use case
    resp, err := h.useCase.Create(user.UserID, req)
    
    // 4. Responder
    json.NewEncoder(w).Encode(resp)
}
```

---

## 3. Flujo de una Petición

Vamos a seguir el flujo cuando un usuario crea una transacción:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CLIENTE                                                       │
│    POST /api/transactions                                        │
│    { "type": "expense", "amount": 1500, ... }                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. HANDLER (handlers/transaction.go)                            │
│    - Extrae userID del JWT (middleware)                         │
│    - Decodifica JSON → dto.CreateTransactionRequest             │
│    - Llama al Use Case                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. USE CASE (usecases/transaction/usecase.go)                  │
│    - Valida que la categoría existe                             │
│    - Crea entidad Transaction                                   │
│    - Llama al Repository                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. REPOSITORY (infrastructure/database/repository.go)          │
│    - Implementa la interfaz TransactionRepository               │
│    - Ejecuta: r.db.Create(transaction)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. GORM / PostgreSQL                                           │
│    - Persiste en la base de datos                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Diagrama de Dependencias

```
handlers/transaction.go
         │
         ▼ usa
transaction.UseCase
         │
         │ usa (interfaz)
         ▼
TransactionRepository (interfaz)
         │
         │ implementa
         ▼
GORMRepository (implementación)
         │
         │ usa
         ▼
PostgreSQL
```

**Nota importante**: Los handlers conocen a los use cases, los use cases conocen a las interfaces de repositories, pero el dominio NO conoce a nadie.

---

## 5. Beneficios de esta Arquitectura

| Beneficio | Ejemplo en el proyecto |
|-----------|----------------------|
| **Testabilidad** | Puedes testear el use case con un mock del repository |
| **Mantenibilidad** | Cambiar de GORM a sqlx solo afecta a infrastructure |
| **Escalabilidad** | Agregar nuevos features es agregar nuevas carpetas |
| **Separación de responsabilidades** | Cada capa tiene un propósito claro |

---

## 6. Cómo agregar una nueva funcionalidad

Imagina que quieres agregar **reportes mensuales**:

1. **Domain**: ¿Necesitas nuevas entidades? Agrégalas en `domain/entities/`
2. **Repository**: ¿Necesitas nuevos métodos? Agrega la firma en `domain/repositories/interfaces.go`
3. **Infrastructure**: Implementa en `infrastructure/database/repository.go`
4. **Use Case**: Crea la lógica en `application/usecases/report/`
5. **DTO**: Crea los objetos request/response en `application/dto/`
6. **Handler**: Crea el endpoint en `handlers/`
7. **Main**: Registra la ruta

---

## 7. Principios Clave Aplicados

### Dependency Inversion
El dominio define interfaces, la infraestructura las implementa. Así el dominio no depende de detalles técnicos.

### Single Responsibility
Cada capa tiene una responsabilidad única:
- **Handler**: Recibir HTTP requests
- **Use Case**: Lógica de negocio
- **Repository**: Acceso a datos

### Dependency Rule
Las dependencias van hacia el centro. Nunca al revés.

---

## 8. Estructura de Archivos

```
cmd/api/main.go
internal/
├── domain/
│   ├── entities/
│   │   └── models.go          # User, Transaction, Category, Tag, Invoice, Product
│   ├── repositories/
│   │   └── interfaces.go     # Contratos (UserRepository, TransactionRepository, etc.)
│   └── valueobjects/
│       └── money.go           # Tipo Money (int64)
│
├── application/
│   ├── dto/
│   │   ├── auth.go            # RegisterRequest, LoginRequest, AuthResponse
│   │   ├── transaction.go     # CreateTransactionRequest, TransactionResponse
│   │   ├── category.go       # CategoryResponse, TagResponse
│   │   └── balance.go        # BalanceResponse
│   │
│   └── usecases/
│       ├── auth/
│       │   └── usecase.go     # Register, Login
│       ├── transaction/
│       │   └── usecase.go    # Create, GetAll, GetByID, Update, Delete
│       ├── category/
│       │   └── usecase.go    # Create, GetAll, GetByID, Update, Delete
│       └── balance/
│           └── usecase.go    # GetBalance
│
├── infrastructure/
│   ├── database/
│   │   ├── database.go       # Conexión a PostgreSQL
│   │   ├── migrations.go    # AutoMigrate
│   │   └── repository.go    # Implementación GORM de los repositorios
│   │
│   ├── auth/
│   │   ├── jwt.go            # Generar y validar JWT
│   │   └── password.go       # Hash de contraseñas (bcrypt)
│   │
│   └── middleware/
│       ├── logger.go         # Logging de requests
│       └── auth.go           # Validación de JWT
│
└── handlers/
    ├── auth.go               # Endpoints: /api/auth/register, /api/auth/login
    ├── transaction.go        # Endpoints: /api/transactions
    ├── category.go           # Endpoints: /api/categories
    └── balance.go           # Endpoints: /api/balance
```

---

## 9. Rutas API

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/api/auth/register` | ❌ | Registro de usuario |
| POST | `/api/auth/login` | ❌ | Login (retorna JWT) |
| GET | `/api/transactions` | ✅ | Listar transacciones |
| POST | `/api/transactions` | ✅ | Crear transacción |
| GET | `/api/transactions/{id}` | ✅ | Obtener transacción |
| PUT | `/api/transactions/{id}` | ✅ | Actualizar transacción |
| DELETE | `/api/transactions/{id}` | ✅ | Eliminar transacción |
| GET | `/api/categories` | ✅ | Listar categorías |
| POST | `/api/categories` | ✅ | Crear categoría |
| GET | `/api/categories/{id}` | ✅ | Obtener categoría |
| PUT | `/api/categories/{id}` | ✅ | Actualizar categoría |
| DELETE | `/api/categories/{id}` | ✅ | Eliminar categoría |
| GET | `/api/balance` | ✅ | Obtener balance |

---

## 10. Resumen Visual

```
 Tu API con Clean Architecture
 ┌────────────────────────────────────────────────────────────┐
 │ cmd/api/main.go                                           │
 │  - Inicializa DB                                          │
 │  - Inicializa JWT                                        │
 │  - Inicializa Use Cases                                  │
 │  - Inicializa Handlers                                   │
 │  - Configura rutas chi.Router                            │
 └────────────────────────────────────────────────────────────┘

 internal/
 ├── handlers/        → ¿Qué recibe el cliente? (HTTP)
 ├── application/     → ¿Qué hace la app? (Lógica)
 ├── domain/          → ¿Qué existe? (Entidades, contratos)
 └── infrastructure/  → ¿Cómo se hace? (DB, Auth)
```

---

## 11. Glosario

| Término | Significado |
|---------|-------------|
| **Entity** | Representa un objeto del dominio (User, Transaction) |
| **Value Object** | Objeto sin identidad propia (Money) |
| **Use Case** | Caso de uso, acción que puede realizar el sistema |
| **Repository** | Interfaz para acceder a datos |
| **DTO** | Data Transfer Object - objeto para transferir datos entre capas |
| **Handler** | Controlador HTTP |
| **Middleware** | Código que se ejecuta entre la request y el handler |
