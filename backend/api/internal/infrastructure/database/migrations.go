package database

import (
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"gorm.io/gorm"
)

func RunMigrations(db *gorm.DB) error {
	return db.AutoMigrate(
		&entities.User{},
		&entities.Category{},
		&entities.Tag{},
		&entities.Transaction{},
		&entities.Invoice{},
		&entities.Product{},
	)
}
