-- Optimización de Base de Datos para Gestor de Finanzas (PostgreSQL)
-- --- EXTENSIONES Y FUNCIONES AUTOMÁTICAS ---
-- Función para actualizar el campo updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- --- TABLAS ---

-- 1. Tabla de Etiquetas (Tags)
CREATE TABLE "tags" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(50) NOT NULL UNIQUE,
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Usuarios
CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(50) NOT NULL UNIQUE,
  "email" VARCHAR(255) NOT NULL UNIQUE,
  "password" VARCHAR(255) NOT NULL,
  "avatar_url" TEXT,
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" TIMESTAMP WITH TIME ZONE -- Borrado lógico para auditoría
);

CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON "users"
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- 3. Tabla de Categorías
CREATE TABLE "categories" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "type" VARCHAR(20) CHECK (type IN ('income', 'expense')),
  "parent_id" INT REFERENCES "categories"("id"),
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" TIMESTAMP WITH TIME ZONE -- Para desactivar categorías sin romper historial
);

CREATE TRIGGER update_categories_updated_at
BEFORE UPDATE ON "categories"
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- 4. Tabla de Transacciones (Módulo Financiero Central)
CREATE TABLE "transactions" (
  "id" SERIAL PRIMARY KEY,
  "code" VARCHAR(100) UNIQUE,
  "type" VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense')),
  "amount" DECIMAL(19, 4) NOT NULL DEFAULT 0,
  "description" TEXT,
  "move_date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "category_id" INT NOT NULL REFERENCES "categories"("id"),
  "user_id" INT NOT NULL REFERENCES "users"("id"),
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" TIMESTAMP WITH TIME ZONE -- Crucial para integridad contable
);

CREATE TRIGGER update_transactions_updated_at
BEFORE UPDATE ON "transactions"
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- 5. Tabla de Facturas (Archivos Digitales)
CREATE TABLE "invoices" (
  "id" SERIAL PRIMARY KEY,
  "transaction_id" INT NOT NULL REFERENCES "transactions"("id") ON DELETE CASCADE,
  "file_name" VARCHAR(255) NOT NULL,
  "file_url" TEXT NOT NULL,
  "mime_type" VARCHAR(100),
  "uploaded_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" TIMESTAMP WITH TIME ZONE -- Saber cuándo se marcó como "borrada" la imagen
);

-- 6. Tabla de Productos (Detalle de Ticket)
CREATE TABLE "products" (
  "id" SERIAL PRIMARY KEY,
  "transaction_id" INT NOT NULL REFERENCES "transactions"("id") ON DELETE CASCADE,
  "name" VARCHAR(255) NOT NULL,
  "price" DECIMAL(19, 4) NOT NULL,
  "quantity" INT NOT NULL DEFAULT 1,
  "shop_name" VARCHAR(255),
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_products_updated_at
BEFORE UPDATE ON "products"
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- --- RELACIONES MUCHOS A MUCHOS ---

CREATE TABLE "user_tags" (
  "user_id" INT REFERENCES "users"("id") ON DELETE CASCADE,
  "tag_id" INT REFERENCES "tags"("id") ON DELETE CASCADE,
  "assigned_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("user_id", "tag_id")
);

CREATE TABLE "category_tags" (
  "category_id" INT REFERENCES "categories"("id") ON DELETE CASCADE,
  "tag_id" INT REFERENCES "tags"("id") ON DELETE CASCADE,
  "assigned_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("category_id", "tag_id")
);

-- --- ÍNDICES PARA RENDIMIENTO ---
CREATE INDEX idx_transactions_user_active ON "transactions"("user_id") WHERE deleted_at IS NULL;
CREATE INDEX idx_users_active ON "users"("email") WHERE deleted_at IS NULL;
CREATE INDEX idx_transactions_date ON "transactions"("move_date");