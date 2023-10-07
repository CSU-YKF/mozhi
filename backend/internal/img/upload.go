package img

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
)

func UploadHandler(c *gin.Context) {
	fmt.Println(c.ContentType())
	file, err := c.FormFile("img")
	if err != nil {
		//TODO
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "upload failed",
		})
	}
	size := file.Size
	name := file.Filename
	c.SaveUploadedFile(file, "/tmp/test.jpg")
	c.JSON(200, gin.H{
		"score":   0,
		"comment": "name: " + name + " size: " + strconv.FormatInt(size, 10),
	})
}
