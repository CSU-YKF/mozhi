package http

import (
	"github.com/gin-gonic/gin"
	"log/slog"
	"mozhi/internal/data"
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
	userId, assessId, imgId, createTime, err := data.GetPublicImgInfo(imgInfoId)
	if err != nil {
		handlleError(c, err)
	} else {
		c.JSON(http.StatusOK, gin.H{
			"userId":     userId,
			"assessId":   assessId,
			"imgId":      imgId,
			"createTime": createTime,
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
		handlleError(c, err)
	} else {
		c.Data(http.StatusOK, "image/jpeg", data)
	}
}
