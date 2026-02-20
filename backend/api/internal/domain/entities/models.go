package entities

import (
	"time"

	"gorm.io/gorm"
)

type Money int64

type Tag struct {
	ID           uint   `gorm:"primaryKey"`
	Name         string `gorm:"type:varchar(50);not null;index:idx_tag_user_name,unique"`
	UserID       *uint  `gorm:"index"`
	CreatedAt    time.Time
	Users        []User        `gorm:"many2many:user_tags;"`
	Categories   []Category    `gorm:"many2many:category_tags;"`
	Transactions []Transaction `gorm:"many2many:transaction_tags;"`
}

type User struct {
	ID           uint    `gorm:"primaryKey"`
	Username     string  `gorm:"type:varchar(50);not null;unique"`
	Email        string  `gorm:"type:varchar(255);not null;unique;index"`
	Password     string  `gorm:"type:varchar(255);not null"`
	AvatarURL    *string `gorm:"type:text"`
	CreatedAt    time.Time
	UpdatedAt    time.Time
	DeletedAt    gorm.DeletedAt `gorm:"index"`
	Transactions []Transaction
	Tags         []Tag `gorm:"many2many:user_tags;"`
}

type Category struct {
	ID        uint      `gorm:"primaryKey"`
	Name      string    `gorm:"type:varchar(100);not null"`
	Type      string    `gorm:"type:varchar(20);not null;check:type IN ('income', 'expense')"`
	ParentID  *uint     `gorm:"index"`
	Parent    *Category `gorm:"foreignKey:ParentID"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Tags      []Tag          `gorm:"many2many:category_tags;"`
}

type Transaction struct {
	ID          uint      `gorm:"primaryKey"`
	Code        *string   `gorm:"type:varchar(100);unique"`
	Type        string    `gorm:"type:varchar(20);not null;check:type IN ('income', 'expense')"`
	Amount      Money     `gorm:"not null;default:0"`
	Currency    string    `gorm:"type:char(3);default:'EUR'"`
	Description string    `gorm:"type:text"`
	MoveDate    time.Time `gorm:"type:date;not null;default:current_date;index"`
	CategoryID  uint      `gorm:"not null;index"`
	UserID      uint      `gorm:"not null;index"`
	CreatedAt   time.Time
	UpdatedAt   time.Time
	DeletedAt   gorm.DeletedAt `gorm:"index"`
	Category    Category       `gorm:"constraint:OnUpdate:CASCADE,OnDelete:RESTRICT;"`
	User        User           `gorm:"constraint:OnUpdate:CASCADE,OnDelete:RESTRICT;"`
	Invoices    []Invoice      `gorm:"foreignKey:TransactionID"`
	Products    []Product      `gorm:"foreignKey:TransactionID"`
	Tags        []Tag          `gorm:"many2many:transaction_tags;"`
}

type Invoice struct {
	ID            uint           `gorm:"primaryKey"`
	TransactionID uint           `gorm:"not null;index"`
	FileName      string         `gorm:"type:varchar(255);not null"`
	FileURL       string         `gorm:"type:text;not null"`
	MimeType      string         `gorm:"type:varchar(100)"`
	UploadedAt    time.Time      `gorm:"autoCreateTime"`
	DeletedAt     gorm.DeletedAt `gorm:"index"`
}

type Product struct {
	ID            uint   `gorm:"primaryKey"`
	TransactionID uint   `gorm:"not null;index"`
	Name          string `gorm:"type:varchar(255);not null"`
	Price         Money  `gorm:"not null"`
	Quantity      int    `gorm:"not null;default:1"`
	ShopName      string `gorm:"type:varchar(255)"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
	DeletedAt     gorm.DeletedAt `gorm:"index"`
}

func (t *Transaction) AfterDelete(tx *gorm.DB) (err error) {
	tx.Model(&Invoice{}).Where("transaction_id = ?", t.ID).Delete(&Invoice{})
	tx.Model(&Product{}).Where("transaction_id = ?", t.ID).Delete(&Product{})
	return
}
