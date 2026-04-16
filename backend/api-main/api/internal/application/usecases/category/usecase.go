package category

import (
	"errors"

	"github.com/vandalieu06/manager-finance/internal/application/dto"
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"github.com/vandalieu06/manager-finance/internal/domain/repositories"
	"gorm.io/gorm"
)

var (
	ErrCategoryNotFound = errors.New("category not found")
)

type UseCase struct {
	repo repositories.CategoryRepository
}

func NewUseCase(repo repositories.CategoryRepository) *UseCase {
	return &UseCase{repo: repo}
}

func (uc *UseCase) Create(req dto.CreateCategoryRequest) (*dto.CategoryResponse, error) {
	category := &entities.Category{
		Name:     req.Name,
		Type:     req.Type,
		ParentID: req.ParentID,
	}

	if err := uc.repo.Create(category); err != nil {
		return nil, err
	}

	resp := dto.ToCategoryResponse(category)
	return &resp, nil
}

func (uc *UseCase) GetByID(id uint) (*dto.CategoryResponse, error) {
	category, err := uc.repo.GetByID(id)
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
	categories, err := uc.repo.GetAll()
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
	categories, err := uc.repo.GetByType(transactionType)
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
	category, err := uc.repo.GetByID(id)
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

	if err := uc.repo.Update(category); err != nil {
		return nil, err
	}

	resp := dto.ToCategoryResponse(category)
	return &resp, nil
}

func (uc *UseCase) Delete(id uint) error {
	category, err := uc.repo.GetByID(id)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return ErrCategoryNotFound
		}
		return err
	}

	return uc.repo.Delete(category.ID)
}
