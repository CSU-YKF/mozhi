package http

import (
	"github.com/gin-gonic/gin"
	"log/slog"
	"math"
	"mozhi/internal/data"
	"mozhi/internal/support"
	"net/http"
	"strconv"
)

func PublicDownloadHandler(c *gin.Context) {
	//get id from json body
	imgInfoId, err := getId(c)
	if err != nil {
		handlleError(c, err)
		return
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
		return
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
	imgId, err := getId(c)
	if err != nil {
		handlleError(c, err)
		return
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
		return
	} else {
		c.Data(http.StatusOK, "image/jpeg", data)
	}
}

func PublicDownloadAssessHandler(c *gin.Context) {
	assessId, err := getId(c)
	if err != nil {
		handlleError(c, err)
		return
	}
	score, comment, err := data.GetAssess(assessId)
	if err != nil {
		handlleError(c, err)
		return
	} else {
		c.JSON(http.StatusOK, gin.H{
			"score":   math.Trunc(float64(score*100)) / 100,
			"comment": comment,
		})
	}
}

func getId(c *gin.Context) (int, error) {
	//get id from json body
	var idStr string
	var id int

	var json struct {
		Id int `json:"id"`
	}
	err := c.ShouldBindJSON(&json)
	id = json.Id
	//JSON匹配失败
	if err != nil {
		if idStr == "" {
			idStr = c.Param("id")
			if idStr == "" {
				idStr = c.Query("id")
				if idStr == "" {
					idStr = c.PostForm("id")
					if idStr == "" {
						slog.Warn("id is empty")
						return 0, &support.InkinError{
							Message:    "id is empty",
							HttpStatus: http.StatusBadRequest,
						}
					}
				}
			}
		}
		id, err = strconv.Atoi(idStr)
		if err != nil {
			slog.Warn(err.Error())
			return 0, &support.InkinError{
				Message:    "id format wrong, try url encode",
				HttpStatus: http.StatusBadRequest,
			}
		}
	}
	return id, nil
}
