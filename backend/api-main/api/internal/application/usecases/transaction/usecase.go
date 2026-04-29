package transaction

import (
	"errors"

	"github.com/vandalieu06/manager-finance/internal/application/dto"
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"github.com/vandalieu06/manager-finance/internal/domain/repositories"
	"gorm.io/gorm"
)

var (
	ErrTransactionNotFound = errors.New("transaction not found")
	ErrUnauthorized        = errors.New("unauthorized")
	ErrCategoryNotFound    = errors.New("category not found")
)

type UseCase struct {
	repo         repositories.TransactionRepository
	categoryRepo repositories.CategoryRepository
}

func NewUseCase(repo repositories.TransactionRepository, categoryRepo repositories.CategoryRepository) *UseCase {
	return &UseCase{repo: repo, categoryRepo: categoryRepo}
}

func (uc *UseCase) Create(userID uint, req dto.CreateTransactionRequest) (*dto.TransactionResponse, error) {
	category, err := uc.categoryRepo.GetByID(req.CategoryID)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, ErrCategoryNotFound
		}
		return nil, err
	}

	transaction := &entities.Transaction{
		Type:        req.Type,
		Amount:      entities.Money(req.Amount),
		Currency:    req.Currency,
		Description: req.Description,
		MoveDate:    req.MoveDate,
		CategoryID:  req.CategoryID,
		UserID:      userID,
		Code:        req.Code,
	}

	if err := uc.repo.Create(transaction); err != nil {
		return nil, err
	}

	transaction.Category = *category

	return &dto.TransactionResponse{
		ID:          transaction.ID,
		Code:        transaction.Code,
		Type:        transaction.Type,
		Amount:      int64(transaction.Amount),
		Currency:    transaction.Currency,
		Description: transaction.Description,
		MoveDate:    transaction.MoveDate,
		CategoryID:  transaction.CategoryID,
		Category:    dto.ToCategoryResponse(category),
		UserID:      transaction.UserID,
		CreatedAt:   transaction.CreatedAt,
		UpdatedAt:   transaction.UpdatedAt,
	}, nil
}

func (uc *UseCase) GetByID(userID, transactionID uint) (*dto.TransactionResponse, error) {
	transaction, err := uc.repo.GetByID(transactionID)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, ErrTransactionNotFound
		}
		return nil, err
	}

	if transaction.UserID != userID {
		return nil, ErrUnauthorized
	}

	resp := dto.ToTransactionResponse(transaction)
	return &resp, nil
}

func (uc *UseCase) GetAllByUserID(userID uint) ([]dto.TransactionResponse, error) {
	transactions, err := uc.repo.GetAllByUserID(userID)
	if err != nil {
		return nil, err
	}

	resp := make([]dto.TransactionResponse, len(transactions))
	for i, t := range transactions {
		resp[i] = dto.ToTransactionResponse(&t)
	}

	return resp, nil
}

func (uc *UseCase) GetByUserIDAndDateRange(userID uint, startDate, endDate string) ([]dto.TransactionResponse, error) {
	transactions, err := uc.repo.GetByUserIDAndDateRange(userID, startDate, endDate)
	if err != nil {
		return nil, err
	}

	resp := make([]dto.TransactionResponse, len(transactions))
	for i, t := range transactions {
		resp[i] = dto.ToTransactionResponse(&t)
	}

	return resp, nil
}

func (uc *UseCase) Update(userID, transactionID uint, req dto.UpdateTransactionRequest) (*dto.TransactionResponse, error) {
	transaction, err := uc.repo.GetByID(transactionID)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, ErrTransactionNotFound
		}
		return nil, err
	}

	if transaction.UserID != userID {
		return nil, ErrUnauthorized
	}

	if req.Type != "" {
		transaction.Type = req.Type
	}
	if req.Amount != 0 {
		transaction.Amount = entities.Money(req.Amount)
	}
	if req.Currency != "" {
		transaction.Currency = req.Currency
	}
	if req.Description != "" {
		transaction.Description = req.Description
	}
	if !req.MoveDate.IsZero() {
		transaction.MoveDate = req.MoveDate
	}
	if req.CategoryID != 0 {
		transaction.CategoryID = req.CategoryID
	}
	if req.Code != nil {
		transaction.Code = req.Code
	}

	if err := uc.repo.Update(transaction); err != nil {
		return nil, err
	}

	resp := dto.ToTransactionResponse(transaction)
	return &resp, nil
}

func (uc *UseCase) Delete(userID, transactionID uint) error {
	transaction, err := uc.repo.GetByID(transactionID)
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return ErrTransactionNotFound
		}
		return err
	}

	if transaction.UserID != userID {
		return ErrUnauthorized
	}

	return uc.repo.Delete(transactionID)
}
