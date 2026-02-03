package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type Book struct {
	ID     string `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
}

var books []Book

func init() {
	books = []Book{
		{ID: "1", Title: "1984", Author: "George Orwell"},
		{ID: "2", Title: "To Kill a Mockingbird", Author: "Harper Lee"},
		{ID: "3", Title: "The Great Gatsby", Author: "F. Scott Fitzgerald"},
	}
}

func loggerMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		client := r.Header.Get("User-Agent")
		log.Printf("[%s] %s - Solicitado desde %s", r.Method, r.URL.Path, client)
		next(w, r)
	}
}

func main() {
	http.HandleFunc("/", loggerMiddleware(homePage))
	http.HandleFunc("/books", loggerMiddleware(getBooks))
	http.HandleFunc("/book", loggerMiddleware(getBook))
	fmt.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Simple REST API in Go!\n")
}

func getBooks(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Metodo no permitido", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(books)
}

func getBook(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id := r.URL.Query().Get("id")
	for _, book := range books {
		if book.ID == id {
			json.NewEncoder(w).Encode(book)
			return
		}
	}
	http.Error(w, "Book not found", http.StatusNotFound)
}

func createBook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Methos not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	var newBook Book
	err := json.NewDecoder(r.Body).Decode(&newBook)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	books = append(books, newBook)
	json.NewEncoder(w).Encode(newBook)
}

// https://opyjo.hashnode.dev/building-a-simple-rest-api-in-go
