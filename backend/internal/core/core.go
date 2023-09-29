package core

import (
	"backend/internal/img"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"strconv"
)

type InitParams struct {
	crt  string
	key  string
	port uint
}

func CreateInitParams() InitParams {
	return InitParams{
		crt:  "server.crt",
		key:  "server.key",
		port: 8888,
	}
}

func Start(params InitParams) {
	e := gin.Default()

	setRoute(e)
	//Run() blocks the execution of the program
	err := e.Run(":" + strconv.Itoa(int(params.port)))
	if err != nil {
		log.Fatal(err)
	}
	//err = e.RunTLS(":"+strconv.Itoa(int(params.port+1)), params.crt, params.key)
	//if err != nil {
	//	log.Fatal(err)
	//}
}

func setRoute(e *gin.Engine) {
	//e.Use(CORSMiddleware())

	e.POST("/api/v1/img/upload", img.UploadHandler)
	e.GET("/api/v1/download")
	e.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "hello world",
		})
	})
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}
