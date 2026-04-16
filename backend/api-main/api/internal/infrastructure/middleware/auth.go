package middleware

import (
	"context"
	"net/http"
	"strings"

	firebase "firebase.google.com/go/v4"
	"firebase.google.com/go/v4/auth"
	"github.com/vandalieu06/manager-finance/internal/domain/repositories"
)

type ContextKey string

const UserContextKey ContextKey = "user"

type FirebaseClaims struct {
	UID         string `json:"uid"`
	Email       string `json:"email"`
	UserID      uint
	FirebaseUID string
}

func AuthMiddleware(firebaseClient *auth.Client, repo repositories.UserRepository) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authHeader := r.Header.Get("Authorization")
			if authHeader == "" {
				http.Error(w, "Authorization header required", http.StatusUnauthorized)
				return
			}

			parts := strings.Split(authHeader, " ")
			if len(parts) != 2 || parts[0] != "Bearer" {
				http.Error(w, "Invalid authorization header format", http.StatusUnauthorized)
				return
			}

			token, err := firebaseClient.VerifyIDToken(r.Context(), parts[1])
			if err != nil {
				http.Error(w, "Invalid Firebase token", http.StatusUnauthorized)
				return
			}

			firebaseUID := token.UID
			email, _ := token.Claims["email"].(string)

			user, err := repo.GetByFirebaseUID(firebaseUID)
			if err != nil {
				http.Error(w, "User not found", http.StatusUnauthorized)
				return
			}

			claims := &FirebaseClaims{
				UID:         firebaseUID,
				Email:       email,
				UserID:      user.ID,
				FirebaseUID: firebaseUID,
			}

			ctx := context.WithValue(r.Context(), UserContextKey, claims)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

func GetUserFromContext(ctx context.Context) *FirebaseClaims {
	user, ok := ctx.Value(UserContextKey).(*FirebaseClaims)
	if !ok {
		return nil
	}
	return user
}

func InitFirebase(app *firebase.App) (*auth.Client, error) {
	return app.Auth(context.Background())
}

func NewFirebaseAuth(app *firebase.App) (*auth.Client, error) {
	return app.Auth(context.Background())
}
