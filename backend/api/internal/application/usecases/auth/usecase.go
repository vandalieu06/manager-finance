package auth

import (
	"errors"
	"time"

	"github.com/vandalieu06/manager-finance/internal/application/dto"
	"github.com/vandalieu06/manager-finance/internal/domain/entities"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/auth"
	"github.com/vandalieu06/manager-finance/internal/infrastructure/database"
)

var (
	ErrUserAlreadyExists  = errors.New("user already exists")
	ErrInvalidCredentials = errors.New("invalid credentials")
)

type UseCase struct {
	repo       *database.Repository
	jwtManager *auth.JWTManager
}

func NewUseCase(repo *database.Repository, jwtManager *auth.JWTManager) *UseCase {
	return &UseCase{
		repo:       repo,
		jwtManager: jwtManager,
	}
}

func (uc *UseCase) Register(req dto.RegisterRequest) (*dto.AuthResponse, error) {
	existingUser, _ := uc.repo.GetByEmail(req.Email)
	if existingUser != nil {
		return nil, ErrUserAlreadyExists
	}

	existingUser, _ = uc.repo.GetByUsername(req.Username)
	if existingUser != nil {
		return nil, ErrUserAlreadyExists
	}

	hashedPassword, err := auth.HashPassword(req.Password)
	if err != nil {
		return nil, err
	}

	user := &entities.User{
		Username: req.Username,
		Email:    req.Email,
		Password: hashedPassword,
	}

	if err := uc.repo.Create(user); err != nil {
		return nil, err
	}

	token, err := uc.jwtManager.Generate(user.ID, user.Username)
	if err != nil {
		return nil, err
	}

	return &dto.AuthResponse{
		Token: token,
		User: dto.UserResponse{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			AvatarURL: user.AvatarURL,
		},
	}, nil
}

func (uc *UseCase) Login(req dto.LoginRequest) (*dto.AuthResponse, error) {
	user, err := uc.repo.GetByEmail(req.Email)
	if err != nil {
		return nil, ErrInvalidCredentials
	}

	if !auth.CheckPassword(req.Password, user.Password) {
		return nil, ErrInvalidCredentials
	}

	token, err := uc.jwtManager.Generate(user.ID, user.Username)
	if err != nil {
		return nil, err
	}

	return &dto.AuthResponse{
		Token: token,
		User: dto.UserResponse{
			ID:        user.ID,
			Username:  user.Username,
			Email:     user.Email,
			AvatarURL: user.AvatarURL,
		},
	}, nil
}

func (uc *UseCase) GetUserByID(id uint) (*dto.UserResponse, error) {
	user, err := uc.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	return &dto.UserResponse{
		ID:        user.ID,
		Username:  user.Username,
		Email:     user.Email,
		AvatarURL: user.AvatarURL,
	}, nil
}

func (uc *UseCase) RefreshToken(userID uint, username string) (string, error) {
	return uc.jwtManager.Generate(userID, username)
}

func (uc *UseCase) ValidateTokenDuration(tokenString string) (time.Duration, error) {
	claims, err := uc.jwtManager.Validate(tokenString)
	if err != nil {
		return 0, err
	}

	expTime := claims.ExpiresAt.Time
	now := time.Now()

	if expTime.Before(now) {
		return 0, errors.New("token expired")
	}

	return expTime.Sub(now), nil
}
