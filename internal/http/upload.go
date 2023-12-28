package http

import (
	"bytes"
	"context"
	"github.com/gin-gonic/gin"
	"github.com/gookit/config/v2"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"image"
	"image/draw"
	_ "image/gif"
	"image/jpeg"
	_ "image/png"
	"log/slog"
	"math"
	"mozhi/internal/data"
	pb "mozhi/internal/rpc/pb"
	"mozhi/internal/support"
	"net/http"
)

func PublicUploadHandler(c *gin.Context) {
	file, _, err := c.Request.FormFile("file")
	if err != nil {
		slog.Error(err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "upload failed, can't form your image type, or have you upload an image? the key is 'file'",
		})
		return
	}
	defer file.Close()
	// Convert the image to three channels
	img, _, err := image.Decode(file)
	if err != nil {
		err = &support.InkinError{
			HttpStatus: http.StatusBadRequest,
			Message:    "can't decode image",
		}
		handlleError(c, err)
		return
	}
	threeChannelImg, err := convertToThreeChannelBytes(img)
	if err != nil {
		handlleError(c, err)
		return
	}

	conn, err := grpc.Dial(config.String("Algorithm.grpcUrl"), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		handlleError(c, err)
		return
	}
	defer conn.Close()
	client := pb.NewAssessServiceClient(conn)
	resp, err := client.Assess(context.Background(), &pb.AssessRequest{
		Img: threeChannelImg,
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
	imgInfoId, imgId, err := data.SaveImg(threeChannelImg, assessId, 0)
	if err != nil {
		handlleError(c, err)
		return
	}
	c.JSON(200, gin.H{
		"score":         math.Trunc(float64(resp.Score*100)) / 100,
		"comment":       resp.Comment,
		"assess_id":     assessId,
		"image_id":      imgId,
		"image_info_id": imgInfoId,
	})
}

func convertToThreeChannelBytes(img image.Image) ([]byte, error) {
	bounds := img.Bounds()
	rgba := image.NewRGBA(bounds)
	draw.Draw(rgba, bounds, img, bounds.Min, draw.Src)
	buf := new(bytes.Buffer)
	err := jpeg.Encode(buf, img, nil)
	if err != nil {
		return nil, err
	}
	return buf.Bytes(), nil
}
