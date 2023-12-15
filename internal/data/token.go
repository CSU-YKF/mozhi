package data

import (
	"crypto/rand"
	"github.com/go-redis/redis/v8"
	"github.com/gookit/config/v2"
	"strconv"
	"time"
)

func getRedisConn() *redis.Client {
	redisClient := redis.NewClient(&redis.Options{
		Addr:     config.String("Redis.addr"),
		Password: config.String("Redis.password"),
		DB:       config.Int("Redis.db"),
	})
	return redisClient
}

func SetToken(userId int) string {
	redisClient := getRedisConn()
	ctx := redisClient.Context()
	token := make([]byte, 32)
	_, _ = rand.Read(token)
	redisClient.Set(ctx, string(token), userId, time.Duration(config.Int("Session.maxAge")))
	return string(token)
}

func TestToken(token string) bool {
	redisClient := getRedisConn()
	ctx := redisClient.Context()
	val, err := redisClient.Get(ctx, token).Result()
	if err != nil {
		return false
	}
	if val == token {
		return true
	} else {
		return false
	}
}
func GetIdByToken(token string) int {
	redisClient := getRedisConn()
	ctx := redisClient.Context()
	val, err := redisClient.Get(ctx, token).Result()
	if err != nil {
		return -1
	}
	res, _ := (strconv.ParseInt(val, 10, 64))
	return int(res)
}
