# 4. Diseño aplicación móvil

## 4.1. Especificación funcional del sistema

Lumen es una aplicación móvil de gestión financiera personal. La versión revisada se centra en la experiencia de usuario móvil y en la construcción de los principales flujos de navegación: acceso a la aplicación, consulta de resumen financiero, listado de productos, captura de facturas, revisión de facturas y configuración de preferencias.

El sistema está desarrollado con Expo y React Native, utilizando Expo Router para organizar la navegación mediante rutas basadas en archivos. La aplicación dispone de una navegación inferior con cuatro secciones principales: Home, Productos, Scan y Configuración. Además, incluye pantallas auxiliares para login, estadísticas, detalle de producto y detalle de factura.

En el estado actual, la app móvil implementa la interfaz principal y la lógica de interacción del prototipo. El login está integrado con Firebase Auth mediante `signInWithEmailAndPassword`; los productos se cargan desde datos estáticos; la captura de facturas utiliza `expo-camera` y envía la imagen a un endpoint HTTP; y el seguimiento/revisión de facturas se apoya en un servicio local en memoria para representar los estados de procesamiento.

## 4.1.1. Especificación del sistema propuesto

El sistema propuesto se organiza alrededor de la actividad del usuario y de sus gastos cotidianos. La aplicación debe permitir consultar información financiera, registrar productos, clasificar gastos y revisar facturas.

En la aplicación móvil actual, las funcionalidades verificadas son:

- Inicio de sesión con Firebase Auth.
- Navegación principal por pestañas.
- Dashboard con tarjetas resumen.
- Pantalla de estadísticas con métricas demostrativas.
- Listado y filtrado de productos.
- Detalle de producto.
- Captura de factura con cámara y envío HTTP de la imagen.
- Revisión de factura con campos detectados y productos asociados.
- Validación o denegación de facturas en memoria.
- Entrada manual de productos vinculados a una factura.
- Configuración básica de perfil y preferencias en estado local.

Las funcionalidades previstas pero no verificadas como implementación final son:

- Registro de nuevos usuarios.
- Recuperación de contraseña.
- Sincronización real con backend.
- Persistencia local offline.
- Respuesta OCR/IA productiva integrada en la revisión de factura.
- Exportación de datos.
- Gestión de presupuestos.
- Área de administración.
- Suscripciones o pagos.

## 4.1.1.1. Descripción de los actores

**Usuario de la aplicación**

Es el actor principal. Accede a la app, consulta información financiera, revisa productos, utiliza el flujo de captura de facturas, añade productos manualmente y modifica preferencias locales.

**Servicio de autenticación externo**

Firebase Auth se encarga de validar las credenciales introducidas en la pantalla de login.

**Servicio local de facturas**

El servicio `src/services/facturas.ts` gestiona en memoria el comportamiento esperado del procesamiento de facturas. Permite listar facturas, obtener una factura por identificador, simular el resultado de procesamiento, añadir productos manuales y cambiar el estado de una factura.

**Servicio HTTP de factura**

El hook `src/hooks/useScanCamera.tsx` usa `expo-camera` para tomar una fotografía y envía la imagen mediante `multipart/form-data` a `/api/factura`. En la versión revisada el endpoint aparece configurado con una URL local de red, por lo que debe ajustarse para cada entorno de ejecución.

```mermaid
graph TD
    USUARIO((Usuario))
    AUTH[Firebase Auth<br/>Servicio externo]
    FACTURAS_SRV[Servicio local<br/>de facturas]
    HTTP_SRV[Servicio HTTP<br/>de factura]
    CAMARA[Cámara del<br/>dispositivo]

    USUARIO -->|Inicia sesión| AUTH
    USUARIO -->|Captura factura| CAMARA
    USUARIO -->|Revisa facturas| FACTURAS_SRV
    USUARIO -->|Añade productos| FACTURAS_SRV
    USUARIO -->|Valida/deniega| FACTURAS_SRV
    CAMARA -->|Envía imagen| HTTP_SRV
```

## 4.1.1.2. Modelo de casos de uso

Los principales casos de uso de la aplicación móvil son:

| Caso de uso | Estado | Descripción |
| --- | --- | --- |
| Iniciar sesión | Implementado | El usuario accede mediante email y contraseña. |
| Consultar dashboard | Implementado con datos demo | Muestra tarjetas resumen y análisis. |
| Ver estadísticas | Implementado con datos demo | Presenta ingresos, beneficios y variación. |
| Listar productos | Implementado con datos demo | Muestra productos definidos en datos estáticos. |
| Buscar productos | Implementado | Permite buscar por nombre, marca, precio, categoría o fecha. |
| Filtrar productos | Implementado | Permite filtrar por categoría, marca y rango de precio. |
| Ver detalle de producto | Implementado | Muestra datos individuales de un producto. |
| Capturar y enviar factura | Implementado parcialmente | Solicita permiso de cámara, toma una imagen y la envía a un endpoint HTTP. |
| Revisar factura | Implementado con datos locales | Muestra campos detectados, productos y estado. |
| Validar o denegar factura | Implementado en memoria | Cambia el estado de la factura. |
| Añadir producto manual | Implementado en memoria | Vincula un producto a una factura existente. |
| Configurar perfil | Implementado localmente | Modifica datos dentro del estado de pantalla. |
| Cambiar preferencias | Implementado localmente | Cambia idioma y controles de preferencias. |
| Cerrar sesión | Implementado | Llama a Firebase Auth mediante `signOut` y redirige a login. |

```mermaid
graph TD
    USUARIO((Usuario))
    USUARIO --> CU_LOGIN[Iniciar sesión]
    USUARIO --> CU_DASH[Consultar dashboard]
    USUARIO --> CU_STATS[Ver estadísticas]
    USUARIO --> CU_LIST[Listar productos]
    USUARIO --> CU_SEARCH[Buscar productos]
    USUARIO --> CU_FILTER[Filtrar productos]
    USUARIO --> CU_DETAIL[Ver detalle producto]
    USUARIO --> CU_SCAN[Capturar y enviar factura]
    USUARIO --> CU_REVIEW[Revisar factura]
    USUARIO --> CU_VALIDATE[Validar o denegar factura]
    USUARIO --> CU_ADD[Añadir producto manual]
    USUARIO --> CU_PROFILE[Configurar perfil]
    USUARIO --> CU_PREFS[Cambiar preferencias]
    USUARIO --> CU_LOGOUT[Cerrar sesión]

    CU_LOGIN -->|depende de| AUTH[Firebase Auth]
    CU_SCAN -->|usa| CAMARA[Cámara dispositivo]
    CU_SCAN -->|envía a| F_ENDPOINT[/api/factura]
```

## 4.1.2. Diseño del sistema

El diseño del sistema se apoya en una separación entre rutas, componentes reutilizables, servicios, datos estáticos, constantes y assets. La carpeta `app/` contiene las pantallas gestionadas por Expo Router, mientras que `src/` agrupa componentes, servicios, dominio, assets y constantes.

```mermaid
graph TD
    subgraph "Expo Router (app/)"
        INDEX[index.tsx<br/>Redirección]
        LOGIN[login.tsx<br/>Autenticación]
        TABS[tabs/<br/>Zona principal]
        STATS[stats.tsx<br/>Estadísticas]
        FACTURAS[facturas/]
    end

    subgraph "Pestañas (tabs/)"
        HOME[index.tsx<br/>Home Dashboard]
        PROD[productos/<br/>Listado + Detalle]
        SCAN[scan/<br/>Captura facturas]
        CONFIG[config/<br/>Ajustes]
    end

    subgraph "src/"
        COMP[components/<br/>UI + Layout]
        SRV[services/<br/>firebase, api, facturas]
        HOOKS[hooks/<br/>useScanCamera]
        DATA[data/<br/>products.ts demo]
        DOMAIN[domain/<br/>types.ts]
        CONST[constants/<br/>colors.js]
        LIB[lib/<br/>i18n.ts]
    end

    INDEX --> LOGIN
    LOGIN --> TABS
    TABS --> HOME
    TABS --> PROD
    TABS --> SCAN
    TABS --> CONFIG
    TABS --> STATS
    SCAN --> FACTURAS
```

## 4.1.2.1. Diagramas de secuencia de los casos de uso más relevantes

**Flujo de inicio de sesión**

1. El usuario introduce email y contraseña.
2. La pantalla de login llama a Firebase Auth.
3. Firebase valida las credenciales.
4. Si la autenticación es correcta, la app redirige a la zona principal.
5. Si falla, se muestra un mensaje de error.

```mermaid
sequenceDiagram
    actor Usuario
    participant Login as Pantalla Login
    participant Firebase as Firebase Auth
    participant App as Zona Principal

    Usuario->>Login: Introduce email + password
    Login->>Firebase: signInWithEmailAndPassword()
    Firebase-->>Login: Token de autenticación
    alt Credenciales correctas
        Login->>App: Redirige a navegación inferior
        App-->>Usuario: Muestra Home
    else Credenciales incorrectas
        Firebase-->>Login: Error de autenticación
        Login-->>Usuario: Muestra mensaje de error
    end
```

**Flujo de captura y revisión de factura**

1. El usuario accede a la pestaña Scan.
2. Selecciona el modo foto.
3. Si no hay permiso de cámara, la app solicita autorización al usuario.
4. La app abre la cámara y permite tomar una fotografía.
5. El usuario revisa la previsualización capturada y confirma el envío.
6. La imagen se envía mediante `multipart/form-data` a `/api/factura`.
7. La interfaz actualiza el estado de factura con el servicio local en memoria.
8. Si existe factura, el usuario puede abrir el detalle.
9. En el detalle, puede validar o denegar la factura.

```mermaid
sequenceDiagram
    actor Usuario
    participant Scan as Pantalla Scan
    participant Camara as expo-camera
    participant Servicio as Servicio facturas
    participant HTTP as HTTP /api/factura

    Usuario->>Scan: Accede a pestaña Scan
    Scan->>Camara: Solicita permiso
    Camara-->>Usuario: Concede permiso
    Usuario->>Camara: Toma fotografía
    Camara-->>Scan: Imagen capturada
    Scan-->>Usuario: Muestra previsualización
    Usuario->>Scan: Confirma envío
    Scan->>HTTP: POST multipart imagen
    HTTP-->>Scan: Respuesta procesamiento
    Scan->>Servicio: Actualiza estado factura
    alt Factura disponible
        Usuario->>Scan: Abre detalle factura
        Scan-->>Usuario: Muestra campos + productos
        Usuario->>Scan: Valida o deniega
        Scan->>Servicio: Cambia estado
    end
```

**Flujo de filtrado de productos**

1. El usuario accede a Productos.
2. La app carga productos de demostración.
3. El usuario aplica filtros o búsqueda.
4. La lista se recalcula en cliente.
5. El usuario puede abrir el detalle de un producto.

```mermaid
sequenceDiagram
    actor Usuario
    participant Prod as Pantalla Productos
    participant Data as Datos demo
    participant Detalle as Detalle producto

    Usuario->>Prod: Accede a Productos
    Prod->>Data: Carga productos
    Data-->>Prod: Lista productos
    Prod-->>Usuario: Muestra listado
    Usuario->>Prod: Introduce búsqueda o filtros
    Prod->>Prod: Filtra en cliente
    Prod-->>Usuario: Lista actualizada
    Usuario->>Prod: Selecciona producto
    Prod->>Detalle: Navega con ID
    Detalle-->>Usuario: Muestra información completa
```

## 4.1.2.2. Diagrama de clases de diseño

Desde el frontend revisado se identifican las siguientes entidades funcionales:

- Producto o gasto registrado.
- Factura.
- Campo detectado de factura.
- Línea de producto de factura.
- Notificación de factura.
- Usuario autenticado.

```mermaid
classDiagram
    class Usuario {
        +string uid
        +string email
        +string nombre
        +login()
        +logout()
    }

    class Producto {
        +int id
        +string nombre
        +string marca
        +float precio
        +string categoria
        +string fecha
    }

    class Factura {
        +int id
        +string estado
        +string comercio
        +float importe
        +string fecha
        +Producto[] productos
        +validar()
        +denegar()
        +addProducto()
    }

    class Categoria {
        +int id
        +string nombre
        +string tipo
    }

    class Notificacion {
        +int id
        +string mensaje
        +string tipo
        +bool leida
    }

    Usuario "1" --> "*" Factura : tiene
    Factura "1" --> "*" Producto : contiene
    Producto "1" --> "1" Categoria : clasifica
    Factura "1" --> "*" Notificacion : genera
    Usuario "1" --> "*" Categoria : gestiona
```

## 4.1.2.3. Diagramas de estado

El caso más representativo es el estado de una factura dentro del flujo de revisión. Una factura puede estar pendiente de revisión, incompleta, validada, denegada o en error.

```mermaid
stateDiagram-v2
    [*] --> Pendiente : Captura realizada
    Pendiente --> Incompleta : Faltan campos
    Pendiente --> Procesando : Enviada a OCR
    Procesando --> Pendiente : OCR completado
    Procesando --> Error : OCR falla
    Incompleta --> Pendiente : Usuario completa
    Pendiente --> Validada : Usuario valida
    Pendiente --> Denegada : Usuario deniega
    Validada --> [*]
    Denegada --> [*]
    Error --> Pendiente : Reintentar
```

## 4.1.3. Interfaces de usuario: mapa de formularios

El mapa de pantallas actual es:

| Pantalla | Ruta | Función |
| --- | --- | --- |
| Entrada inicial | `app/index.tsx` | Redirección inicial. |
| Login | `app/login.tsx` | Autenticación. |
| Home | `app/(tabs)/index.tsx` | Resumen financiero. |
| Productos | `app/(tabs)/productos/index.tsx` | Listado y filtros. |
| Detalle de producto | `app/(tabs)/productos/[id].tsx` | Información individual. |
| Scan | `app/(tabs)/scan/index.tsx` | Captura de factura y entrada manual. |
| Detalle de factura | `app/facturas/[id].tsx` | Revisión y validación. |
| Stats | `app/stats.tsx` | Estadísticas. |
| Configuración | `app/(tabs)/config/index.tsx` | Opciones de usuario. |
| Perfil | `app/(tabs)/config/perfil.tsx` | Edición local de perfil. |
| Preferencias | `app/(tabs)/config/preferencias.tsx` | Idioma, moneda y tema. |
| Notificaciones | `app/(tabs)/config/notificaciones.tsx` | Interruptores locales de recordatorios, resumen y push. |
| Categorías | `app/(tabs)/config/categorias.tsx` | Pantalla base de categorías. |
| Datos | `app/(tabs)/config/datos.tsx` | Acciones de importar, sincronizar y exportar pendientes de CSV. |
| Información | `app/(tabs)/config/informacion.tsx` | Información de la aplicación. |

```mermaid
graph TD
    INDEX[index.tsx<br/>Redirección]
    LOGIN[login.tsx<br/>Login Firebase]
    TABS[tabs/_layout.tsx<br/>Navegación inferior]
    HOME[index.tsx<br/>Home]
    PROD[productos/index.tsx<br/>Listado productos]
    PROD_DET[productos/[id].tsx<br/>Detalle producto]
    SCAN[scan/index.tsx<br/>Captura factura]
    FACTURA[facturas/[id].tsx<br/>Detalle factura]
    STATS[stats.tsx<br/>Estadísticas]
    CONFIG[config/index.tsx<br/>Menú configuración]
    PERFIL[config/perfil.tsx<br/>Perfil]
    PREF[config/preferencias.tsx<br/>Preferencias]
    NOTIF[config/notificaciones.tsx<br/>Notificaciones]
    CAT[config/categorias.tsx<br/>Categorías]
    DATOS[config/datos.tsx<br/>Datos]
    INFO[config/informacion.tsx<br/>Información]

    INDEX --> LOGIN
    LOGIN --> TABS
    TABS --> HOME
    TABS --> PROD
    TABS --> SCAN
    TABS --> CONFIG
    TABS --> STATS
    PROD --> PROD_DET
    SCAN --> FACTURA
    CONFIG --> PERFIL
    CONFIG --> PREF
    CONFIG --> NOTIF
    CONFIG --> CAT
    CONFIG --> DATOS
    CONFIG --> INFO
```

## 4.2. Bases de datos

La base de datos del sistema es relacional y está gestionada mediante **PostgreSQL 17** con **GORM** como ORM. El esquema se define mediante los modelos GORM y se aplica automáticamente mediante `AutoMigrate` al iniciar el backend. No se utiliza `init.sql`: la fuente de verdad es el código.

> La aplicación móvil no dispone de base de datos local. Trabaja con datos de demostración estáticos y stores en memoria. Toda la persistencia real recae en el backend Go con PostgreSQL.

## 4.2.1. Modelo Entidad-Relación (E/R)

```mermaid
erDiagram
    USER ||--o{ TRANSACTION : "has"
    USER }o--o{ TAG : "user_tags"
    CATEGORY ||--o{ TRANSACTION : "categorizes"
    TRANSACTION ||--o{ INVOICE : "has"
    TRANSACTION ||--o{ PRODUCT : "contains"
    TRANSACTION }o--o{ TAG : "transaction_tags"

    USER {
        uint id PK
        string firebase_uid "unique"
        string username
        string email "unique"
        string avatar_url "nullable"
        string currency "default EUR"
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }

    CATEGORY {
        uint id PK
        string name "not null"
        string type "income | expense"
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }

    TAG {
        uint id PK
        string name "unique with user"
        uint user_id FK "nullable = global"
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }

    TRANSACTION {
        uint id PK
        string code "unique, nullable"
        string type "income | expense"
        int64 amount "centavos"
        string currency "default EUR"
        string description
        string company "comercio"
        date move_date "not null, indexed"
        bool is_ocr_processed "default false"
        uint category_id FK "not null"
        uint user_id FK "not null"
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }

    INVOICE {
        uint id PK
        uint transaction_id FK "not null"
        string file_name "not null"
        string file_url "not null"
        string mime_type
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }

    PRODUCT {
        uint id PK
        uint transaction_id FK "not null"
        string name "not null"
        int64 price "centavos"
        int quantity "default 1"
        string shop_name
        datetime created_at
        datetime updated_at
        datetime deleted_at "soft delete"
    }
```

## 4.2.2. Esquema lógico normalizado (3FN)

### Tablas principales

#### `users`

Almacena los usuarios del sistema. Se autentican mediante Firebase Auth y se identifican por `firebase_uid`.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | Identificador único |
| `firebase_uid` | `varchar(128)` | Unique, not null, indexed | UID de Firebase Auth |
| `username` | `varchar(50)` | | Nombre de usuario visible |
| `email` | `varchar(255)` | Unique, not null, indexed | Correo electrónico |
| `avatar_url` | `text` | Nullable | URL del avatar |
| `currency` | `char(3)` | Default: `'EUR'` | Moneda preferida del usuario |
| `created_at` | `timestamp` | Not null | Fecha de creación |
| `updated_at` | `timestamp` | Not null | Fecha de actualización |
| `deleted_at` | `timestamp` | Nullable (soft delete) | Fecha de borrado lógico |

#### `categories`

Clasificación de los movimientos financieros en dos tipos: ingresos y gastos.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | Identificador único |
| `name` | `varchar(100)` | Not null | Nombre visible (ej. "Alimentación") |
| `type` | `varchar(20)` | Not null, check: `IN ('income', 'expense')` | Tipo de categoría |
| `created_at` | `timestamp` | Not null | |
| `updated_at` | `timestamp` | Not null | |
| `deleted_at` | `timestamp` | Nullable (soft delete) | |

#### `tags`

Etiquetas universales o por usuario que permiten clasificar transacciones con criterios adicionales.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | Identificador único |
| `name` | `varchar(50)` | Not null, unique (con user_id) | Nombre de la etiqueta |
| `user_id` | `uint` | Nullable, FK → users.id | Null = tag global |
| `created_at` | `timestamp` | Not null | |
| `updated_at` | `timestamp` | Not null | |
| `deleted_at` | `timestamp` | Nullable (soft delete) | |

#### `transactions`

Entidad principal del dominio. Representa cada movimiento financiero registrado.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | Identificador único |
| `code` | `varchar(100)` | Unique, nullable | Código del ticket o factura |
| `type` | `varchar(20)` | Not null, check: `IN ('income', 'expense')` | Tipo de movimiento |
| `amount` | `int64` | Not null, default: 0 | Importe en **céntimos** |
| `currency` | `char(3)` | Default: `'EUR'` | Moneda |
| `description` | `text` | | Descripción libre |
| `company` | `varchar(255)` | | Nombre del comercio (ej. "Mercadona") |
| `move_date` | `date` | Not null, default: current_date, indexed | Fecha del movimiento |
| `is_ocr_processed` | `bool` | Default: false | Indica si se procesó con OCR |
| `category_id` | `uint` | Not null, FK → categories.id | Categoría del movimiento |
| `user_id` | `uint` | Not null, FK → users.id | Propietario de la transacción |
| `created_at` | `timestamp` | Not null | |
| `updated_at` | `timestamp` | Not null | |
| `deleted_at` | `timestamp` | Nullable (soft delete) | |

> **Importe en céntimos:** El campo `amount` usa el tipo `Money` (int64) para evitar errores de redondeo con punto flotante. Un valor de 1500 representa 15,00 €.

#### `invoices`

Facturas o tickets asociados a una transacción. Almacenan la imagen del ticket original.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | |
| `transaction_id` | `uint` | Not null, FK → transactions.id | Transacción asociada |
| `file_name` | `varchar(255)` | Not null | Nombre original del archivo |
| `file_url` | `text` | Not null | Ruta relativa en disco |
| `mime_type` | `varchar(100)` | | Tipo MIME del archivo |
| `created_at` | `timestamp` | Not null | |
| `updated_at` | `timestamp` | Not null | |
| `deleted_at` | `timestamp` | Nullable (soft delete) | |

#### `products`

Líneas de producto extraídas de una factura. Se generan automáticamente mediante el flujo OCR o se añaden manualmente.

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | `uint` | PK, auto-incremento | |
| `transaction_id` | `uint` | Not null, FK → transactions.id | Transacción asociada |
| `name` | `varchar(255)` | Not null | Nombre del producto |
| `price` | `int64` | Not null | Precio en céntimos |
| `quantity` | `int` | Not null, default: 1 | Cantidad |
| `shop_name` | `varchar(255)` | | Nombre del comercio |
| `created_at` | `timestamp` | Not null | |
| `updated_at` | `timestamp` | Not null | |
| `deleted_at` | `timestamp` | Nullable (soft delete) | |

### Tablas pivote (many-to-many)

#### `user_tags`

Asocia usuarios con tags. Un usuario puede tener muchas tags; una tag puede pertenecer a muchos usuarios.

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `user_id` | `uint` | FK → users.id |
| `tag_id` | `uint` | FK → tags.id |

**Clave primaria:** compuesta `(user_id, tag_id)`.

#### `transaction_tags`

Asocia transacciones con tags. Una transacción puede tener muchas tags; una tag puede aparecer en muchas transacciones.

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `transaction_id` | `uint` | FK → transactions.id |
| `tag_id` | `uint` | FK → tags.id |

**Clave primaria:** compuesta `(transaction_id, tag_id)`.

### Resumen de relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| User → Transaction | 1:N | Un usuario tiene muchas transacciones |
| User → Tag | M:N | Tabla pivote `user_tags` |
| Category → Transaction | 1:N | Una categoría clasifica muchas transacciones |
| Transaction → Invoice | 1:N | Una transacción tiene varias facturas |
| Transaction → Product | 1:N | Una transacción contiene varios productos |
| Transaction → Tag | M:N | Tabla pivote `transaction_tags` |

### Integridad referencial

| Restricción | Regla |
|-------------|-------|
| `transactions.category_id` → `categories.id` | `ON UPDATE CASCADE`, `ON DELETE RESTRICT` |
| `transactions.user_id` → `users.id` | `ON UPDATE CASCADE`, `ON DELETE RESTRICT` |
| `invoices.transaction_id` → `transactions.id` | Borrado en cascada mediante hook `AfterDelete` de GORM |
| `products.transaction_id` → `transactions.id` | Borrado en cascada mediante hook `AfterDelete` de GORM |

### Notas sobre GORM

- **Soft delete:** Todas las entidades usan `gorm.Model`, que incluye `DeletedAt`. Las consultas estándar excluyen automáticamente los registros borrados.
- **AutoMigrate:** Al arrancar, el backend ejecuta `db.AutoMigrate(User, Category, Tag, Transaction, Invoice, Product)`. Crea tablas, añade columnas faltantes y crea índices. No elimina columnas ni tablas existentes.
- **Hook AfterDelete:** Al eliminar una transacción, GORM ejecuta un hook que borra en cascada las facturas y productos asociados.

## 4.3. Diseño de la interfaz

La interfaz de Lumen aplica una estética de alto contraste, con influencia brutalista. Los elementos se presentan como bloques sólidos, con bordes negros marcados y sombras duras. Esta decisión visual conecta con el concepto de marca: aportar claridad sobre el comportamiento financiero del usuario.

## 4.3.1. Prototipado

El prototipado en Figma incluye pantallas de Home Dashboard y Productos. También se han definido tokens de diseño, componentes base y especificaciones para futuras pantallas como Configuración y Escanear Facturas.

Prototipo disponible en `docs/figma/01-home/SPEC.md` (especificación completa).

Prototipo disponible en `docs/figma/04-productos/SPEC.md` (especificación completa).

Prototipo disponible en `docs/figma/03-escanear-facturas/SPEC.md` (especificación completa).

Prototipo disponible en `docs/figma/02-configuracion/SPEC.md` (especificación completa).

## 4.3.2. Guía de estilo

La guía visual se basa en los siguientes elementos:

- Tipografía principal: Red Hat Mono.
- Tipografía secundaria: Inter para navegación o gráficos cuando sea necesario.
- Bordes negros de 3px o 4px.
- Sombras duras sin desenfoque decorativo.
- Paleta centralizada en tokens de color.
- Categorías principales: obligación, ahorro y ocio.

| Grupo | Uso | Colores principales |
| --- | --- | --- |
| Primary | Acciones principales | `#4ECDC4` |
| Secondary | Contraste y acciones secundarias | `#F76132` |
| Accent | Destacados visuales | `#FFE66D`, `#FF6B6B`, `#F7FFF7` |
| Feedback | Estados | `#22C55E`, `#EF4444`, `#F59E0B`, `#0EA5E9` |
| Category | Clasificación de gastos | `#4F46E5`, `#10B981`, `#A855F7` |
| Base | Fondo y contraste | `#FFFFFF`, `#000000` |

Pendiente de insertar captura del sistema de diseño.
