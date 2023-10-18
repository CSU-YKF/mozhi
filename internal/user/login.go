package user

import (
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"log/slog"
	"mozhi/internal/data"
)

func LoginHandler(c *gin.Context) {
	db := data.GetDb()
	defer db.Close()
	{
		token, err := c.Cookie(config.String("Session.cookieName"))
		if err == nil {
			if data.TestToken(token) {
				c.JSON(200, gin.H{
					"msg": "already login",
				})
				return
			}
		}
	}

	name := c.PostForm("username")
	password := c.PostForm("password")
	if name == "" || password == "" {
		c.JSON(400, gin.H{
			"msg": "username or password is empty",
		})
		return
	}
	stmt, err := db.Prepare("SELECT id, saltpassword FROM user WHERE name = ?")
	if err != nil {
		slog.Error(err.Error())
		return
	}
	var salt string
	var saltpassword string
	var id int
	err = stmt.QueryRow(name).Scan(&id, &salt, &saltpassword)
	if err != nil {
		slog.Warn(err.Error())
		return
	}
	if saltpassword == data.CryptoPassword(salt, password) {
		c.JSON(200, gin.H{
			"msg": "login success",
		})
		token := data.SetToken(id)

		c.SetCookie(config.String("Session.cookieName"), token, config.Int("Session.maxAge"), config.String("Session.path"), config.String("Session.domain"), config.Bool("Session.secure"), config.Bool("Session.httpOnly"))
		return
	} else {
		c.JSON(200, gin.H{
			"msg": "login failed",
		})
		return
	}
}
