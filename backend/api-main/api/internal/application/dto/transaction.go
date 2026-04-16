package dto

import (
	"time"

	"github.com/vandalieu06/manager-finance/internal/domain/entities"
)

type CreateTransactionRequest struct {
	Type        string    `json:"type" validate:"required,oneof=income expense"`
	Amount      int64     `json:"amount" validate:"required"`
	Currency    string    `json:"currency" validate:"required,len=3"`
	Description string    `json:"description"`
	MoveDate    time.Time `json:"move_date" validate:"required"`
	CategoryID  uint      `json:"category_id" validate:"required"`
	Code        *string   `json:"code,omitempty"`
	TagIDs      []uint    `json:"tag_ids,omitempty"`
}

type UpdateTransactionRequest struct {
	Type        string    `json:"type" validate:"omitempty,oneof=income expense"`
	Amount      int64     `json:"amount"`
	Currency    string    `json:"currency" validate:"omitempty,len=3"`
	Description string    `json:"description"`
	MoveDate    time.Time `json:"move_date"`
	CategoryID  uint      `json:"category_id"`
	Code        *string   `json:"code,omitempty"`
	TagIDs      []uint    `json:"tag_ids,omitempty"`
}

type TransactionResponse struct {
	ID          uint             `json:"id"`
	Code        *string          `json:"code,omitempty"`
	Type        string           `json:"type"`
	Amount      int64            `json:"amount"`
	Currency    string           `json:"currency"`
	Description string           `json:"description"`
	MoveDate    time.Time        `json:"move_date"`
	CategoryID  uint             `json:"category_id"`
	Category    CategoryResponse `json:"category,omitempty"`
	UserID      uint             `json:"user_id"`
	Tags        []TagResponse    `json:"tags,omitempty"`
	CreatedAt   time.Time        `json:"created_at"`
	UpdatedAt   time.Time        `json:"updated_at"`
}

func ToTransactionResponse(t *entities.Transaction) TransactionResponse {
	resp := TransactionResponse{
		ID:          t.ID,
		Code:        t.Code,
		Type:        t.Type,
		Amount:      int64(t.Amount),
		Currency:    t.Currency,
		Description: t.Description,
		MoveDate:    t.MoveDate,
		CategoryID:  t.CategoryID,
		UserID:      t.UserID,
		CreatedAt:   t.CreatedAt,
		UpdatedAt:   t.UpdatedAt,
	}

	if t.Category.ID != 0 {
		resp.Category = ToCategoryResponse(&t.Category)
	}

	resp.Tags = make([]TagResponse, len(t.Tags))
	for i, tag := range t.Tags {
		resp.Tags[i] = ToTagResponse(&tag)
	}

	return resp
}
