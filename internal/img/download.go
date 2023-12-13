package img

import (
	"errors"
	"github.com/gin-gonic/gin"
	"log/slog"
	"mozhi/internal/data"
	"mozhi/internal/support"
	"net/http"
	"strconv"
)

func PublicDownloadHandler(c *gin.Context) {
	//get id from json body
	var id string
	var imgInfoId int

	var json struct {
		Id int `json:"id"`
	}
	err := c.ShouldBindJSON(&json)
	imgInfoId = json.Id
	//JSON匹配失败
	if err != nil {
		if id == "" {
			id = c.Param("id")
			if id == "" {
				id = c.Query("id")
				if id == "" {
					id = c.PostForm("id")
					slog.Warn("no id")
					return
				}
			}
		}
		imgInfoId, err = strconv.Atoi(id)
	}

	if err != nil {
		slog.Warn(err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "id is not a number",
		})
	}
	userId, assessId, imgId, err := data.GetPublicImgInfo(imgInfoId)
	if err != nil {
		slog.Warn(err.Error())
		var inkinErr *support.InkinError
		if errors.As(err, &inkinErr) {
			// 如果错误是InkinError类型，返回一个特定的响应
			c.JSON(inkinErr.HttpStatus, gin.H{
				"msg": inkinErr.Message,
			})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "server error",
			})
		}
	} else {
		c.JSON(http.StatusOK, gin.H{
			"userId":   userId,
			"assessId": assessId,
			"imgId":    imgId,
		})
	}
}

func PublicDownloadImageHandler(c *gin.Context) {
	//get id from json body
	var id string
	var imgId int

	var json struct {
		Id int `json:"id"`
	}
	err := c.ShouldBindJSON(&json)
	imgId = json.Id
	//JSON匹配失败
	if err != nil {
		if id == "" {
			id = c.Param("id")
			if id == "" {
				id = c.Query("id")
				if id == "" {
					id = c.PostForm("id")
					slog.Warn("no id")
					return
				}
			}
		}
		imgId, err = strconv.Atoi(id)
	}

	if err != nil {
		slog.Warn(err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "id is not a number",
		})
	}
	data, err := data.GetPublicImg(imgId)
	if err != nil {
		slog.Warn(err.Error())
		var inkinErr *support.InkinError
		if errors.As(err, &inkinErr) {
			// 如果错误是InkinError类型，返回一个特定的响应
			c.JSON(inkinErr.HttpStatus, gin.H{
				"msg": inkinErr.Message,
			})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{
				"msg": "server error",
			})
		}
	} else {
		c.Data(http.StatusOK, "image/jpeg", data)
	}
}
