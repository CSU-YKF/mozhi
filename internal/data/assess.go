package data

import (
	"log/slog"
	"mozhi/internal/support"
)

func SaveAssess(userId int, score float32, comment string) (id int64, err error) {
	db := GetDb()
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO assess (user_id, score, comment) VALUES (?,?,?)")
	if err != nil {
		slog.Error(err.Error())
		return 0, &support.InkinError{Message: "Database error", HttpStatus: 500}
	}
	res, err := stmt.Exec(userId, score, comment)
	if err != nil {
		slog.Error(err.Error())
		return 0, &support.InkinError{Message: "Database error", HttpStatus: 500}
	}
	id, err = res.LastInsertId()
	if err != nil {
		slog.Error(err.Error())
		return 0, &support.InkinError{Message: "Database error", HttpStatus: 500}
	}
	return id, nil
}

func GetAssess(id int) (score float32, comment string, err error) {
	db := GetDb()
	defer db.Close()

	stmt, err := db.Prepare("SELECT score, comment FROM assess WHERE id = ? and user_id = 0")
	if err != nil {
		slog.Error(err.Error())
		return 0, "", &support.InkinError{Message: "Database error", HttpStatus: 500}
	}
	rows, err := stmt.Query(id)
	if err != nil {
		slog.Error(err.Error())
		return 0, "", &support.InkinError{Message: "Database error", HttpStatus: 500}
	}
	for rows.Next() {
		err = rows.Scan(&score, &comment)
		if err != nil {
			slog.Error(err.Error())
			return 0, "", &support.InkinError{Message: "Database error", HttpStatus: 500}
		}
	}
	return score, comment, nil
}
