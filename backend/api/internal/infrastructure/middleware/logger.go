package middleware

import (
	"log"
	"net/http"
)

func LoggerMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		client := r.Header.Get("User-Agent")
		log.Printf("[%s] %s - Solicitado desde %s", r.Method, r.URL.Path, client)
		next(w, r)
	}
}
