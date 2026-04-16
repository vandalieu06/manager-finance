package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type TransactionRepository struct {
	db *gorm.DB
}

func NewTransactionRepository(db *gorm.DB) *TransactionRepository {
	return &TransactionRepository{db: db}
}

func (r *TransactionRepository) Create(transaction *entities.Transaction) error {
	return r.db.Create(transaction).Error
}

func (r *TransactionRepository) GetByID(id uint) (*entities.Transaction, error) {
	var transaction entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").First(&transaction, id).Error
	if err != nil {
		return nil, err
	}
	return &transaction, nil
}

func (r *TransactionRepository) GetAllByUserID(userID uint) ([]entities.Transaction, error) {
	var transactions []entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").
		Where("user_id = ?", userID).
		Order("move_date DESC").
		Find(&transactions).Error
	return transactions, err
}

func (r *TransactionRepository) GetByUserIDAndDateRange(userID uint, startDate, endDate string) ([]entities.Transaction, error) {
	var transactions []entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").
		Where("user_id = ? AND move_date BETWEEN ? AND ?", userID, startDate, endDate).
		Order("move_date DESC").
		Find(&transactions).Error
	return transactions, err
}

func (r *TransactionRepository) Update(transaction *entities.Transaction) error {
	return r.db.Save(transaction).Error
}

func (r *TransactionRepository) Delete(id uint) error {
	return r.db.Delete(&entities.Transaction{}, id).Error
}
