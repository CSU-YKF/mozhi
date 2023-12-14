package http

import (
	"github.com/gin-gonic/gin"
	"mozhi/internal/data"
)

func PublicDownloadIdListHandler(c *gin.Context) {
	jsonStr, err := data.GetPublicInfoList()
	if err != nil {
		handlleError(c, err)
		return
	}
	c.Data(200, "application/json", []byte(jsonStr))
}
