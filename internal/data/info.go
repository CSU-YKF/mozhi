package data

import (
	"encoding/json"
	"log"
	"log/slog"
	"mozhi/internal/support"
)

type ImageInfo struct {
	ID         int    `json:"id"`
	ImgID      int    `json:"img_id"`
	AssessID   int    `json:"assess_id"`
	CreateTime string `json:"create_time"`
}

func GetPublicInfoList() (jsonStr string, err error) {
	db := GetDb()
	defer db.Close()

	rows, err := db.Query("SELECT ID, img_id, assess_id, create_time FROM image_info WHERE user_id = 0")
	if err != nil {
		slog.Error(err.Error())
		return "", &support.InkinError{
			Message:    "database error",
			HttpStatus: 500,
		}
	}
	defer rows.Close()

	var infos []ImageInfo
	for rows.Next() {
		var info ImageInfo
		err := rows.Scan(&info.ID, &info.ImgID, &info.AssessID, &info.CreateTime)
		if err != nil {
			log.Fatal(err)
		}
		infos = append(infos, info)
	}

	if err := rows.Err(); err != nil {
		log.Fatal(err)
	}

	jsonData, err := json.Marshal(infos)
	if err != nil {
		log.Fatal(err)
	}

	return string(jsonData), nil
}
