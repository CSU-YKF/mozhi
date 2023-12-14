package main

import (
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/yaml"
	"log"
	"mozhi/internal/core"
	"os"
	"time"
)

func main() {
	initConfig := core.InitConfig{}
	dataBaseConfig := core.DatabaseConfig{}
	redisConfig := core.RedisConfig{}
	sessionConfig := core.SessionConfig{}
	algorithmConfig := core.AlgorithmConfig{}

	gin.SetMode(gin.ReleaseMode)
	// 设置选项支持 ENV 解析
	config.WithOptions(config.ParseEnv)

	// 添加驱动程序以支持yaml内容解析（除了JSON是默认支持，其他的则是按需使用）
	config.AddDriver(yaml.Driver)

	// 加载配置，可以同时传入多个文件
	err := config.LoadFiles("./config.yaml")
	err = config.LoadFiles("./config/config.yaml")
	if err != nil {
		panic(err)
	}

	err = config.BindStruct("Init", &initConfig)
	if err != nil {
		panic(err)
	}
	err = config.BindStruct("Database", &dataBaseConfig)
	if err != nil {
		panic(err)
	}
	err = config.BindStruct("Redis", &redisConfig)
	if err != nil {
		panic(err)
	}
	err = config.BindStruct("Session", &sessionConfig)
	if err != nil {
		panic(err)
	}
	err = config.BindStruct("Algorithm", &algorithmConfig)
	if err != nil {
		panic(err)
	}

	// 获取当前日期
	currentTime := time.Now()

	// 格式化日期，例如 "2006-01-02.log"
	logFileName := "./log/" + currentTime.Format("2006-01-02_15-04-05") + ".log"

	// 创建 log 文件夹
	err = os.MkdirAll("log", 0755)
	if err != nil {
		log.Fatal(err)
	}
	// 打开一个文件
	logFile, err := os.OpenFile(logFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}

	// 设置 log 的输出到这个文件
	log.SetOutput(logFile)

	// 现在，这些信息会写入以当前日期命名的日志文件
	log.Println("Starting the application...")

	core.Start()
}
