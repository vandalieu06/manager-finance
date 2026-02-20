package category

import (
	"errors"

	"github.com/vandalieu06/manager-finance/internal/application/dto"
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/database"
	"gorm.io/gorm"
)

var (
	ErrCategoryNotFound = errors.New("category not found")
)

type UseCase struct {
	repo *database.Repository
}

func NewUseCase(repo *database.Repository) *UseCase {
	return &UseCase{repo: repo}
}

func (uc *UseCase) Create(req dto.CreateCategoryRequest) (*dto.CategoryResponse, error) {
	category := &entities.Category{
		Name:     req.Name,
		Type:     req.Type,
		ParentID: req.ParentID,
	}

	if err := uc.repo.CreateCategory(category); err != nil {
		return nil, err
	}

	resp := dto.ToCategoryResponse(category)
	return &resp, nil
}

func (uc *UseCase) GetByID(id uint) (*dto.CategoryResponse, error) {
	category, err := uc.repo.GetCategoryByID(id)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, ErrCategoryNotFound
		}
		return nil, err
	}

	resp := dto.ToCategoryResponse(category)
	return &resp, nil
}

func (uc *UseCase) GetAll() ([]dto.CategoryResponse, error) {
	categories, err := uc.repo.GetAllCategories()
	if err != nil {
		return nil, err
	}

	resp := make([]dto.CategoryResponse, len(categories))
	for i, c := range categories {
		resp[i] = dto.ToCategoryResponse(&c)
	}

	return resp, nil
}

func (uc *UseCase) GetByType(transactionType string) ([]dto.CategoryResponse, error) {
	categories, err := uc.repo.GetCategoriesByType(transactionType)
	if err != nil {
		return nil, err
	}

	resp := make([]dto.CategoryResponse, len(categories))
	for i, c := range categories {
		resp[i] = dto.ToCategoryResponse(&c)
	}

	return resp, nil
}

func (uc *UseCase) Update(id uint, req dto.UpdateCategoryRequest) (*dto.CategoryResponse, error) {
	category, err := uc.repo.GetCategoryByID(id)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, ErrCategoryNotFound
		}
		return nil, err
	}

	if req.Name != "" {
		category.Name = req.Name
	}
	if req.Type != "" {
		category.Type = req.Type
	}
	if req.ParentID != nil {
		category.ParentID = req.ParentID
	}

	if err := uc.repo.UpdateCategory(category); err != nil {
		return nil, err
	}

	resp := dto.ToCategoryResponse(category)
	return &resp, nil
}

func (uc *UseCase) Delete(id uint) error {
	category, err := uc.repo.GetCategoryByID(id)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return ErrCategoryNotFound
		}
		return err
	}

	return uc.repo.DeleteCategory(category.ID)
}
