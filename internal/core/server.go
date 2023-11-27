package core

import (
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"log"
	"mozhi/internal/img"
	"mozhi/internal/user"
	"strconv"
)

func Start() {
	e := gin.Default()

	setRoute(e)
	//Run() blocks the execution of the program
	err := e.Run(":" + strconv.Itoa(config.Int("Init.port")))
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

	root := "../../" + config.String("Init.static")
	e.Static("/", root)
	e.POST("/api/v1/public/img/upload", img.UploadHandler)
	e.POST("/register", user.RegisterHandler)
	e.POST("/login", user.LoginHandler)
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
