package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/vandalieu06/manager-finance/internal/application/usecases/balance"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/middleware"
)

type BalanceHandler struct {
	useCase *balance.UseCase
}

func NewBalanceHandler(useCase *balance.UseCase) *BalanceHandler {
	return &BalanceHandler{useCase: useCase}
}

func (h *BalanceHandler) GetBalance(w http.ResponseWriter, r *http.Request) {
	user := middleware.GetUserFromContext(r.Context())
	if user == nil {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	currency := r.URL.Query().Get("currency")
	if currency == "" {
		currency = "EUR"
	}

	resp, err := h.useCase.GetBalance(user.UserID, currency)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
