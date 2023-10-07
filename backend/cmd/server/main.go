package main

import "backend/internal/core"

func main() {
	param := core.CreateInitParams()
	core.Start(param)
}
