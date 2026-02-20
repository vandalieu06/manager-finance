package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	authUseCase "github.com/vandalieu06/manager-finance/internal/application/usecases/auth"
	balanceUseCase "github.com/vandalieu06/manager-finance/internal/application/usecases/balance"
	categoryUseCase "github.com/vandalieu06/manager-finance/internal/application/usecases/category"
	transactionUseCase "github.com/vandalieu06/manager-finance/internal/application/usecases/transaction"
	"github.com/vandalieu06/manager-finance/internal/handlers"
	authInfra "github.com/vandalieu06/manager-finance/internal/infrastructure/auth"
	db "github.com/vandalieu06/manager-finance/internal/infrastructure/database"
	mw "github.com/vandalieu06/manager-finance/internal/infrastructure/middleware"
)

func main() {
	database := db.NewConnection()

	if err := db.RunMigrations(database); err != nil {
		log.Fatalf("Error running migrations: %v", err)
	}

	repo := db.NewRepository(database)

	jwtManager := authInfra.NewJWTManager("your-secret-key-change-in-production", 24*time.Hour)

	authUC := authUseCase.NewUseCase(repo, jwtManager)
	transactionUC := transactionUseCase.NewUseCase(repo)
	categoryUC := categoryUseCase.NewUseCase(repo)
	balanceUC := balanceUseCase.NewUseCase(repo)

	authHandler := handlers.NewAuthHandler(authUC)
	transactionHandler := handlers.NewTransactionHandler(transactionUC)
	categoryHandler := handlers.NewCategoryHandler(categoryUC)
	balanceHandler := handlers.NewBalanceHandler(balanceUC)

	r := chi.NewRouter()

	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("API de Gestión de Finanzas Personales"))
	})

	r.Route("/api/auth", func(r chi.Router) {
		r.Mount("/", authHandler.Routes())
	})

	r.Route("/api/transactions", func(r chi.Router) {
		r.Use(mw.AuthMiddleware(jwtManager))
		r.Mount("/", transactionHandler.Routes())
	})

	r.Route("/api/categories", func(r chi.Router) {
		r.Use(mw.AuthMiddleware(jwtManager))
		r.Mount("/", categoryHandler.Routes())
	})

	r.Route("/api/balance", func(r chi.Router) {
		r.Use(mw.AuthMiddleware(jwtManager))
		r.Get("/", balanceHandler.GetBalance)
	})

	fmt.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", r))
}
