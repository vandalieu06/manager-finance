package dto

type BalanceResponse struct {
	TotalIncome  int64  `json:"total_income"`
	TotalExpense int64  `json:"total_expense"`
	Balance      int64  `json:"balance"`
	Currency     string `json:"currency"`
}
