package core

import (
	"bytes"
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"io"
	"log"
	"log/slog"
	"mozhi/internal/img"
	"mozhi/internal/user"
	"strconv"
)

func Start() {
	e := gin.Default()

	setRoute(e)
	//Run() blocks the execution of the program
	slog.Info("server starting at port " + strconv.Itoa(config.Int("Init.port")))
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
	e.Use(CORSMiddleware())
	e.Use(logMiddleware())

	//root := "../../" + config.String("Init.static")
	root := config.String("Init.static")

	e.GET("/test", test)
	e.POST("/api/v1/public/img/upload", img.PublicUploadHandler)
	e.GET("/api/v1/public/imginfo/get", img.PublicDownloadHandler)
	e.GET("/api/v1/public/img/get", img.PublicDownloadImageHandler)
	e.POST("/api/v1/register", user.RegisterHandler)
	e.POST("/api/v1/login", user.LoginHandler)
	e.Static("/home", root)
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

func logMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		bodyBytes, err := io.ReadAll(c.Request.Body)
		if err != nil {
			slog.Warn("Failed to read request body")
			return
		}
		// 将body的内容复制回c.Request.Body，以便后面的代码可以读取它
		c.Request.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

		slog.Info(
			"Receiving Request",
			"Request IP", c.ClientIP(),
			"Request Host", c.Request.Host,
			"Request URL", c.Request.URL.Path,
			"Request Method", c.Request.Method,
			"Request Header", c.Request.Header,
			"Request Body", string(bodyBytes), // 打印body的内容
			"Request Form", c.Request.Form,
		)
		c.Next()
	}
}

func test(c *gin.Context) {
	c.JSON(200, gin.H{
		"msg": "test success",
	})
}
