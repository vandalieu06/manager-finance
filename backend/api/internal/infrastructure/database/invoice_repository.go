package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type InvoiceRepository struct {
	db *gorm.DB
}

func NewInvoiceRepository(db *gorm.DB) *InvoiceRepository {
	return &InvoiceRepository{db: db}
}

func (r *InvoiceRepository) Create(invoice *entities.Invoice) error {
	return r.db.Create(invoice).Error
}

func (r *InvoiceRepository) GetByTransactionID(transactionID uint) ([]entities.Invoice, error) {
	var invoices []entities.Invoice
	err := r.db.Where("transaction_id = ?", transactionID).Find(&invoices).Error
	return invoices, err
}

func (r *InvoiceRepository) Delete(id uint) error {
	return r.db.Delete(&entities.Invoice{}, id).Error
}
