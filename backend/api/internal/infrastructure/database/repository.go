package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type Repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) Create(user *entities.User) error {
	return r.db.Create(user).Error
}

func (r *Repository) GetByID(id uint) (*entities.User, error) {
	var user entities.User
	err := r.db.First(&user, id).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *Repository) GetByEmail(email string) (*entities.User, error) {
	var user entities.User
	err := r.db.Where("email = ?", email).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *Repository) GetByUsername(username string) (*entities.User, error) {
	var user entities.User
	err := r.db.Where("username = ?", username).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *Repository) Update(user *entities.User) error {
	return r.db.Save(user).Error
}

func (r *Repository) Delete(id uint) error {
	return r.db.Delete(&entities.User{}, id).Error
}

func (r *Repository) CreateTransaction(transaction *entities.Transaction) error {
	return r.db.Create(transaction).Error
}

func (r *Repository) GetTransactionByID(id uint) (*entities.Transaction, error) {
	var transaction entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").First(&transaction, id).Error
	if err != nil {
		return nil, err
	}
	return &transaction, nil
}

func (r *Repository) GetAllTransactionsByUserID(userID uint) ([]entities.Transaction, error) {
	var transactions []entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").Where("user_id = ?", userID).Order("move_date DESC").Find(&transactions).Error
	return transactions, err
}

func (r *Repository) GetTransactionsByUserIDAndDateRange(userID uint, startDate, endDate string) ([]entities.Transaction, error) {
	var transactions []entities.Transaction
	err := r.db.Preload("Category").Preload("Tags").
		Where("user_id = ? AND move_date BETWEEN ? AND ?", userID, startDate, endDate).
		Order("move_date DESC").
		Find(&transactions).Error
	return transactions, err
}

func (r *Repository) UpdateTransaction(transaction *entities.Transaction) error {
	return r.db.Save(transaction).Error
}

func (r *Repository) DeleteTransaction(id uint) error {
	return r.db.Delete(&entities.Transaction{}, id).Error
}

func (r *Repository) CreateCategory(category *entities.Category) error {
	return r.db.Create(category).Error
}

func (r *Repository) GetCategoryByID(id uint) (*entities.Category, error) {
	var category entities.Category
	err := r.db.First(&category, id).Error
	if err != nil {
		return nil, err
	}
	return &category, nil
}

func (r *Repository) GetAllCategories() ([]entities.Category, error) {
	var categories []entities.Category
	err := r.db.Where("parent_id IS NULL").Preload("Tags").Find(&categories).Error
	return categories, err
}

func (r *Repository) GetCategoriesByType(transactionType string) ([]entities.Category, error) {
	var categories []entities.Category
	err := r.db.Where("type = ? AND parent_id IS NULL", transactionType).Find(&categories).Error
	return categories, err
}

func (r *Repository) UpdateCategory(category *entities.Category) error {
	return r.db.Save(category).Error
}

func (r *Repository) DeleteCategory(id uint) error {
	return r.db.Delete(&entities.Category{}, id).Error
}

func (r *Repository) CreateTag(tag *entities.Tag) error {
	return r.db.Create(tag).Error
}

func (r *Repository) GetTagByID(id uint) (*entities.Tag, error) {
	var tag entities.Tag
	err := r.db.First(&tag, id).Error
	if err != nil {
		return nil, err
	}
	return &tag, nil
}

func (r *Repository) GetAllTags() ([]entities.Tag, error) {
	var tags []entities.Tag
	err := r.db.Find(&tags).Error
	return tags, err
}

func (r *Repository) GetTagsByUserID(userID *uint) ([]entities.Tag, error) {
	var tags []entities.Tag
	var err error
	if userID == nil {
		err = r.db.Where("user_id IS NULL").Find(&tags).Error
	} else {
		err = r.db.Where("user_id IS NULL OR user_id = ?", *userID).Find(&tags).Error
	}
	return tags, err
}

func (r *Repository) DeleteTag(id uint) error {
	return r.db.Delete(&entities.Tag{}, id).Error
}

func (r *Repository) CreateInvoice(invoice *entities.Invoice) error {
	return r.db.Create(invoice).Error
}

func (r *Repository) GetInvoicesByTransactionID(transactionID uint) ([]entities.Invoice, error) {
	var invoices []entities.Invoice
	err := r.db.Where("transaction_id = ?", transactionID).Find(&invoices).Error
	return invoices, err
}

func (r *Repository) DeleteInvoice(id uint) error {
	return r.db.Delete(&entities.Invoice{}, id).Error
}

func (r *Repository) CreateProduct(product *entities.Product) error {
	return r.db.Create(product).Error
}

func (r *Repository) GetProductsByTransactionID(transactionID uint) ([]entities.Product, error) {
	var products []entities.Product
	err := r.db.Where("transaction_id = ?", transactionID).Find(&products).Error
	return products, err
}

func (r *Repository) DeleteProduct(id uint) error {
	return r.db.Delete(&entities.Product{}, id).Error
}
