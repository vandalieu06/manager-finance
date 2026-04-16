package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	firebase "firebase.google.com/go/v4"
	"github.com/go-chi/chi/v5"
	chiMiddleware "github.com/go-chi/chi/v5/middleware"
	"github.com/vandalieu06/manager-finance/internal/application/usecases/balance"
	"github.com/vandalieu06/manager-finance/internal/application/usecases/category"
	"github.com/vandalieu06/manager-finance/internal/application/usecases/transaction"
	"github.com/vandalieu06/manager-finance/internal/handlers"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/database"
	appMiddleware "github.com/vandalieu06/manager-finance/internal/infrastructure/middleware"
	"google.golang.org/api/option"

	_ "github.com/joho/godotenv/autoload"
)

func main() {
	ctx := context.Background()
	db := database.NewConnection()

	if err := database.RunMigrations(db); err != nil {
		log.Fatalf("Error running migrations: %v", err)
	}

	userRepo := database.NewUserRepository(db)
	transactionRepo := database.NewTransactionRepository(db)
	categoryRepo := database.NewCategoryRepository(db)
	tagRepo := database.NewTagRepository(db)
	invoiceRepo := database.NewInvoiceRepository(db)
	productRepo := database.NewProductRepository(db)

	_ = tagRepo
	_ = invoiceRepo
	_ = productRepo

	firebaseApp, err := firebase.NewApp(ctx, nil, option.WithCredentialsFile(os.Getenv("FIREBASE_CREDENTIALS")))
	if err != nil {
		log.Fatalf("Error initializing Firebase: %v", err)
	}

	firebaseClient, err := appMiddleware.InitFirebase(firebaseApp)
	if err != nil {
		log.Fatalf("Error initializing Firebase Auth: %v", err)
	}

	transactionUC := transaction.NewUseCase(transactionRepo, categoryRepo)
	categoryUC := category.NewUseCase(categoryRepo)
	balanceUC := balance.NewUseCase(transactionRepo)

	transactionHandler := handlers.NewTransactionHandler(transactionUC)
	categoryHandler := handlers.NewCategoryHandler(categoryUC)
	balanceHandler := handlers.NewBalanceHandler(balanceUC)

	r := chi.NewRouter()

	r.Use(chiMiddleware.Logger)
	r.Use(chiMiddleware.Recoverer)

	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("API de Gestión de Finanzas Personales"))
	})

	r.Route("/api/transactions", func(r chi.Router) {
		r.Use(appMiddleware.AuthMiddleware(firebaseClient, userRepo))
		r.Mount("/", transactionHandler.Routes())
	})

	r.Route("/api/categories", func(r chi.Router) {
		r.Use(appMiddleware.AuthMiddleware(firebaseClient, userRepo))
		r.Mount("/", categoryHandler.Routes())
	})

	r.Route("/api/balance", func(r chi.Router) {
		r.Use(appMiddleware.AuthMiddleware(firebaseClient, userRepo))
		r.Get("/", balanceHandler.GetBalance)
	})

	fmt.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", r))
}
