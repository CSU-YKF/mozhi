package img

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
	"io"
	"log/slog"
	pb "mozhi/internal/rpc/pb"
	"net/http"
)

func UploadHandler(c *gin.Context) {
	fmt.Println(c.ContentType())
	file, err := c.FormFile("img")
	if err != nil {
		//TODO
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "upload failed",
		})
	}
	fileObject, err := file.Open()
	if err != nil {
		slog.Warn(err.Error())
	}
	defer fileObject.Close()
	content, err := io.ReadAll(fileObject)

	conn, err := grpc.Dial("localhost:50051")
	if err != nil {
		slog.Warn(err.Error())
	}
	defer conn.Close()
	client := pb.NewAssessServiceClient(conn)
	resp, err := client.Assess(context.Background(), &pb.AssessRequest{
		Img: content,
	})

	c.SaveUploadedFile(file, "/tmp/test.jpg")
	c.JSON(200, gin.H{
		"score":   resp.Score,
		"comment": resp.Comment,
	})
}
