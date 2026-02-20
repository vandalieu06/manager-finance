package valueobjects

type Money int64

func NewMoney(amount int64) Money {
	return Money(amount)
}

func (m Money) Amount() int64 {
	return int64(m)
}

func (m Money) ToFloat64() float64 {
	return float64(m) / 100
}

func FromFloat64(amount float64) Money {
	return Money(int64(amount * 100))
}
