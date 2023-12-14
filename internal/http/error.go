package http

import (
	"errors"
	"github.com/gin-gonic/gin"
	"log/slog"
	"mozhi/internal/support"
	"net/http"
)

func handlleError(c *gin.Context, err error) {
	if err != nil {
		slog.Warn(err.Error())
		var inkinErr *support.InkinError
		if errors.As(err, &inkinErr) {
			// 如果错误是InkinError类型，返回一个特定的响应
			c.JSON(inkinErr.HttpStatus, gin.H{
				"msg": inkinErr.Message,
			})
			return
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "server error",
			})
			return
		}
	}
}
