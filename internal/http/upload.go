package http

import (
	"context"
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"io"
	"log/slog"
	"mozhi/internal/data"
	pb "mozhi/internal/rpc/pb"
	"net/http"
)

func PublicUploadHandler(c *gin.Context) {
	imgForm, err := c.FormFile("file")
	if err != nil {
		slog.Error(err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "upload failed, can't form your image type, or have you upload an image? the key is 'file'",
		})
		return
	}
	fileObject, err := imgForm.Open()
	if err != nil {
		slog.Warn(err.Error())

	}
	defer fileObject.Close()
	content, err := io.ReadAll(fileObject)

	conn, err := grpc.Dial(config.String("Algorithm.grpcUrl"), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		slog.Warn(err.Error())
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": "server grpc failed",
		})
		return
	}
	defer conn.Close()
	client := pb.NewAssessServiceClient(conn)
	resp, err := client.Assess(context.Background(), &pb.AssessRequest{
		Img: content,
	})
	if err != nil {
		slog.Warn(err.Error())
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": "server grpc failed",
		})
		return
	}
	assessId, err := data.SaveAssess(0, resp.Score, resp.Comment)
	if err != nil {
		handlleError(c, err)
		return
	}
	imgInfoId, imgId, err := data.SaveImg(content, assessId, 0)
	if err != nil {
		handlleError(c, err)
		return
	}
	c.JSON(200, gin.H{
		"score":         resp.Score,
		"comment":       resp.Comment,
		"assess_id":     assessId,
		"image_id":      imgId,
		"image_info_id": imgInfoId,
	})
}
