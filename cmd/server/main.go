package main

import (
	"github.com/gookit/config/v2"
	"github.com/gookit/config/v2/yaml"
	"mozhi/internal/core"
)

func main() {
	initConfig := core.InitConfig{}

	// 设置选项支持 ENV 解析
	config.WithOptions(config.ParseEnv)

	// 添加驱动程序以支持yaml内容解析（除了JSON是默认支持，其他的则是按需使用）
	config.AddDriver(yaml.Driver)

	// 加载配置，可以同时传入多个文件
	err := config.LoadFiles("../../config/config.yaml")
	if err != nil {
		panic(err)
	}

	err = config.BindStruct("Init", &initConfig)
	if err != nil {
		panic(err)
	}

	core.Start()
}
