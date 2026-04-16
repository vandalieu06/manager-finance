package repositories

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
)

type UserRepository interface {
	Create(user *entities.User) error
	GetByID(id uint) (*entities.User, error)
	GetByEmail(email string) (*entities.User, error)
	GetByUsername(username string) (*entities.User, error)
	GetByFirebaseUID(firebaseUID string) (*entities.User, error)
	Update(user *entities.User) error
	Delete(id uint) error
}

type TransactionRepository interface {
	Create(transaction *entities.Transaction) error
	GetByID(id uint) (*entities.Transaction, error)
	GetAllByUserID(userID uint) ([]entities.Transaction, error)
	GetByUserIDAndDateRange(userID uint, startDate, endDate string) ([]entities.Transaction, error)
	Update(transaction *entities.Transaction) error
	Delete(id uint) error
}

type CategoryRepository interface {
	Create(category *entities.Category) error
	GetByID(id uint) (*entities.Category, error)
	GetAll() ([]entities.Category, error)
	GetByType(transactionType string) ([]entities.Category, error)
	Update(category *entities.Category) error
	Delete(id uint) error
}

type TagRepository interface {
	Create(tag *entities.Tag) error
	GetByID(id uint) (*entities.Tag, error)
	GetAll() ([]entities.Tag, error)
	GetByUserID(userID *uint) ([]entities.Tag, error)
	Delete(id uint) error
}

type InvoiceRepository interface {
	Create(invoice *entities.Invoice) error
	GetByTransactionID(transactionID uint) ([]entities.Invoice, error)
	Delete(id uint) error
}

type ProductRepository interface {
	Create(product *entities.Product) error
	GetByTransactionID(transactionID uint) ([]entities.Product, error)
	Delete(id uint) error
}
