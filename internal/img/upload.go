package img

import (
	"context"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"io"
	"log/slog"
	"mozhi/internal/data"
	pb "mozhi/internal/rpc/pb"
	"net/http"
)

func PublicUploadHandler(c *gin.Context) {
	imgForm, err := c.FormFile("img")
	if err != nil {
		//TODO
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "upload failed",
		})
	}
	fileObject, err := imgForm.Open()
	if err != nil {
		slog.Warn(err.Error())

	}
	defer fileObject.Close()
	content, err := io.ReadAll(fileObject)

	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		slog.Warn(err.Error())
		c.JSON(http.StatusInternalServerError, gin.H{
			"msg": "server grpc failed",
		})
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
	}
	//TODO
	data.SaveImg(content, 0, 0)
	c.JSON(200, gin.H{
		"score":   resp.Score,
		"comment": resp.Comment,
	})
}
