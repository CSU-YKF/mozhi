package core

type InitConfig struct {
	crt        string `mapstructure:"crt"`
	key        string `mapstructure:"key"`
	port       uint   `mapstructure:"port"`
	rpc_client string `mapstructure:"rpc_client"`
	rpc_server string `mapstructure:"rpc_server"`
	static     string `mapstructure:"static"`
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

type AlgorithmConfig struct {
	grpcUrl string `mapstructure:"grpcUrl"`
}
