package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type CategoryRepository struct {
	db *gorm.DB
}

func NewCategoryRepository(db *gorm.DB) *CategoryRepository {
	return &CategoryRepository{db: db}
}

func (r *CategoryRepository) Create(category *entities.Category) error {
	return r.db.Create(category).Error
}

func (r *CategoryRepository) GetByID(id uint) (*entities.Category, error) {
	var category entities.Category
	err := r.db.First(&category, id).Error
	if err != nil {
		return nil, err
	}
	return &category, nil
}

func (r *CategoryRepository) GetAll() ([]entities.Category, error) {
	var categories []entities.Category
	err := r.db.Where("parent_id IS NULL").Preload("Tags").Find(&categories).Error
	return categories, err
}

func (r *CategoryRepository) GetByType(transactionType string) ([]entities.Category, error) {
	var categories []entities.Category
	err := r.db.Where("type = ? AND parent_id IS NULL", transactionType).Find(&categories).Error
	return categories, err
}

func (r *CategoryRepository) Update(category *entities.Category) error {
	return r.db.Save(category).Error
}

func (r *CategoryRepository) Delete(id uint) error {
	return r.db.Delete(&entities.Category{}, id).Error
}
