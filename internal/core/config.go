package core

type InitConfig struct {
	crt    string `mapstructure:"crt"`
	key    string `mapstructure:"key"`
	port   uint   `mapstructure:"port"`
	static string `mapstructure:"static"`
}
