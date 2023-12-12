package user

import (
	"github.com/gin-gonic/gin"
	"log/slog"
	"mozhi/internal/data"
)

func RegisterHandler(c *gin.Context) {
	db := data.GetDb()
	defer db.Close()
	name := c.PostForm("username")
	stmt, err := db.Prepare("SELECT 1 FROM user WHERE name = ?")
	if err != nil {
		slog.Error(err.Error())
	}
	res, err := stmt.Exec(name)
	if err != nil {
		slog.Warn(err.Error())
	}
	if res != nil {
		c.JSON(200, gin.H{
			"msg": "username already exists",
		})
		return
	}

	nickname := name
	salt := data.GenerateSalt()
	password := c.PostForm("password")
	if name == "" || password == "" {
		c.JSON(200, gin.H{
			"msg": "username or password is empty",
		})
		return
	}

	saltpassword := data.CryptoPassword(salt, c.PostForm("password"))
	stmt, err = db.Prepare("INSERT INTO user(name, nickname, salt, saltpassword) VALUES(?,?,?,?)")
	if err != nil {
		slog.Error(err.Error())
		return
	}
	res, err = stmt.Exec(name, nickname, salt, saltpassword)
	if err != nil {
		slog.Warn(err.Error())
		return
	}
	if res != nil {
		c.JSON(200, gin.H{
			"msg": "register success",
		})
		return
	}
}
