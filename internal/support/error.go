package support

// 自定义的错误类型
type InkinError struct {
	Message    string
	HttpStatus int
}

// 实现error接口
func (e *InkinError) Error() string {
	return e.Message
}

func (e *InkinError) Info() (string, int) {
	return e.Message, e.HttpStatus
}
