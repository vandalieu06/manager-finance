package balance

import (
	"github.com/vandalieu06/manager-finance/internal/application/dto"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/database"
)

type UseCase struct {
	repo *database.Repository
}

func NewUseCase(repo *database.Repository) *UseCase {
	return &UseCase{repo: repo}
}

func (uc *UseCase) GetBalance(userID uint, currency string) (*dto.BalanceResponse, error) {
	transactions, err := uc.repo.GetAllTransactionsByUserID(userID)
	if err != nil {
		return nil, err
	}

	var totalIncome int64
	var totalExpense int64

	for _, t := range transactions {
		if t.Currency != currency {
			continue
		}

		amount := int64(t.Amount)

		switch t.Type {
		case "income":
			totalIncome += amount
		case "expense":
			totalExpense += amount
		}
	}

	return &dto.BalanceResponse{
		TotalIncome:  totalIncome,
		TotalExpense: totalExpense,
		Balance:      totalIncome - totalExpense,
		Currency:     currency,
	}, nil
}

func (uc *UseCase) GetBalanceByDateRange(userID uint, currency, startDate, endDate string) (*dto.BalanceResponse, error) {
	transactions, err := uc.repo.GetTransactionsByUserIDAndDateRange(userID, startDate, endDate)
	if err != nil {
		return nil, err
	}

	var totalIncome int64
	var totalExpense int64

	for _, t := range transactions {
		if t.Currency != currency {
			continue
		}

		amount := int64(t.Amount)

		switch t.Type {
		case "income":
			totalIncome += amount
		case "expense":
			totalExpense += amount
		}
	}

	return &dto.BalanceResponse{
		TotalIncome:  totalIncome,
		TotalExpense: totalExpense,
		Balance:      totalIncome - totalExpense,
		Currency:     currency,
	}, nil
}
