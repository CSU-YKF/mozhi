package main

import (
	"context"
	"flag"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log/slog"
	pb "mozhi/internal/rpc/pb"
)

func main() {
	content := flag.String("img", "", "path to img")

	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		slog.Warn(err.Error())
	}
	defer conn.Close()
	client := pb.NewAssessServiceClient(conn)
	resp, err := client.Assess(context.Background(), &pb.AssessRequest{
		Img: []byte(*content),
	})
	if err != nil {
		slog.Warn(err.Error())
	}
	println(resp.Score)
	println(resp.Comment)
}
