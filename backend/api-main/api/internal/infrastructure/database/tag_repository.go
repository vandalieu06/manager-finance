package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

type TagRepository struct {
	db *gorm.DB
}

func NewTagRepository(db *gorm.DB) *TagRepository {
	return &TagRepository{db: db}
}

func (r *TagRepository) Create(tag *entities.Tag) error {
	return r.db.Create(tag).Error
}

func (r *TagRepository) GetByID(id uint) (*entities.Tag, error) {
	var tag entities.Tag
	err := r.db.First(&tag, id).Error
	if err != nil {
		return nil, err
	}
	return &tag, nil
}

func (r *TagRepository) GetAll() ([]entities.Tag, error) {
	var tags []entities.Tag
	err := r.db.Find(&tags).Error
	return tags, err
}

func (r *TagRepository) GetByUserID(userID *uint) ([]entities.Tag, error) {
	var tags []entities.Tag
	var err error
	if userID == nil {
		err = r.db.Where("user_id IS NULL").Find(&tags).Error
	} else {
		err = r.db.Where("user_id IS NULL OR user_id = ?", *userID).Find(&tags).Error
	}
	return tags, err
}

func (r *TagRepository) Delete(id uint) error {
	return r.db.Delete(&entities.Tag{}, id).Error
}
