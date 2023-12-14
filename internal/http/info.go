package http

import (
	"github.com/gin-gonic/gin"
	"mozhi/internal/data"
)

func PublicDownloadIdListHandler(c *gin.Context) {
	jsonStr, err := data.GetPublicInfoList()
	handlleError(c, err)
	c.Data(200, "application/json", []byte(jsonStr))
}
