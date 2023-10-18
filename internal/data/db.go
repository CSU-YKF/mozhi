package data

import (
	"crypto/rand"
	"crypto/sha256"
	"database/sql"
	"github.com/gookit/config/v2"
	"log"
	// "time"

	_ "github.com/go-sql-driver/mysql"
)

func GetDb() *sql.DB {
	db, err := sql.Open(config.String("Database.driverName"), config.String("Database.dataSource"))
	if err != nil {
		log.Fatal(err)
	}
	return db
}

func GenerateSalt() string {
	salt := make([]byte, 16)
	rand.Read(salt)
	return string(salt)
}

func CryptoPassword(salt string, password string) string {
	sum := sha256.Sum256([]byte(salt + password))
	return string(sum[:])
}
