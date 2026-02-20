package dto

import (
	"time"

	"github.com/vandalieu06/manager-finance/internal/domain/entities"
)

type CreateCategoryRequest struct {
	Name     string `json:"name" validate:"required,min=1,max=100"`
	Type     string `json:"type" validate:"required,oneof=income expense"`
	ParentID *uint  `json:"parent_id,omitempty"`
}

type UpdateCategoryRequest struct {
	Name     string `json:"name" validate:"omitempty,min=1,max=100"`
	Type     string `json:"type" validate:"omitempty,oneof=income expense"`
	ParentID *uint  `json:"parent_id,omitempty"`
}

type CategoryResponse struct {
	ID        uint               `json:"id"`
	Name      string             `json:"name"`
	Type      string             `json:"type"`
	ParentID  *uint              `json:"parent_id,omitempty"`
	Tags      []TagResponse      `json:"tags,omitempty"`
	Children  []CategoryResponse `json:"children,omitempty"`
	CreatedAt time.Time          `json:"created_at"`
	UpdatedAt time.Time          `json:"updated_at"`
}

func ToCategoryResponse(c *entities.Category) CategoryResponse {
	resp := CategoryResponse{
		ID:        c.ID,
		Name:      c.Name,
		Type:      c.Type,
		ParentID:  c.ParentID,
		CreatedAt: c.CreatedAt,
		UpdatedAt: c.UpdatedAt,
	}

	resp.Tags = make([]TagResponse, len(c.Tags))
	for i, tag := range c.Tags {
		resp.Tags[i] = ToTagResponse(&tag)
	}

	return resp
}

type TagResponse struct {
	ID     uint   `json:"id"`
	Name   string `json:"name"`
	UserID *uint  `json:"user_id,omitempty"`
}

func ToTagResponse(t *entities.Tag) TagResponse {
	return TagResponse{
		ID:     t.ID,
		Name:   t.Name,
		UserID: t.UserID,
	}
}
