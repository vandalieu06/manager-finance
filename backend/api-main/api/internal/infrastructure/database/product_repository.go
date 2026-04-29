package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type ProductRepository struct {
	db *gorm.DB
}

func NewProductRepository(db *gorm.DB) *ProductRepository {
	return &ProductRepository{db: db}
}

func (r *ProductRepository) Create(product *entities.Product) error {
	return r.db.Create(product).Error
}

func (r *ProductRepository) GetByTransactionID(transactionID uint) ([]entities.Product, error) {
	var products []entities.Product
	err := r.db.Where("transaction_id = ?", transactionID).Find(&products).Error
	return products, err
}

func (r *ProductRepository) Delete(id uint) error {
	return r.db.Delete(&entities.Product{}, id).Error
}
