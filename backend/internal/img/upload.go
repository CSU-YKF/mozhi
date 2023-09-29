package img

import "github.com/gin-gonic/gin"

func UploadHandler(c *gin.Context) {
	c.Header("Access-Control-Allow-Origin", "*")
	c.Set("Content-Type", "application/json")
	c.String(200, "hello world")
	c.FileAttachment(".", "YFK.svg")
}
