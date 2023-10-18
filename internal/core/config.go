package core

type InitConfig struct {
	crt    string `mapstructure:"crt"`
	key    string `mapstructure:"key"`
	port   uint   `mapstructure:"port"`
	static string `mapstructure:"static"`
}

type DatabaseConfig struct {
	dataSource string `mapstructure:"dataSource"`
	driverName string `mapstructure:"driverName"`
}

type RedisConfig struct {
	addr     string `mapstructure:"addr"`
	password string `mapstructure:"password"`
	db       int    `mapstructure:"db"`
}

type SessionConfig struct {
	name     string `mapstructure:"name"`
	maxAge   int    `mapstructure:"maxAge"`
	path     string `mapstructure:"path"`
	domain   string `mapstructure:"domain"`
	secure   bool   `mapstructure:"secure"`
	httpOnly bool   `mapstructure:"httpOnly"`
}
