package data

import (
	"crypto/md5"
	"encoding/hex"
	_ "github.com/go-sql-driver/mysql"
	"log/slog"
)

func SaveImg(img []byte, assessId int64, userId int64) (imageInfoId int64, imageId int64, err error) {
	db := GetDb()
	defer db.Close()

	// 开始一个事务
	tx, err := db.Begin()
	if err != nil {
		slog.Error(err.Error())
		return 0, 0, err
	}

	// 计算图片的MD5
	hasher := md5.New()
	hasher.Write(img)
	imgMd5 := hex.EncodeToString(hasher.Sum(nil))
	var dataId int64

	// 检查图片是否已经存在
	stmt, _ := tx.Prepare("SELECT img_id FROM image_info WHERE md5 = ?")
	rows, err := stmt.Query(imgMd5)
	if err != nil {
		slog.Error(err.Error())
		tx.Rollback()
		return 0, 0, err
	}
	if rows.Next() {
		err = rows.Scan(&dataId)
		if err != nil {
			slog.Error(err.Error())
			tx.Rollback()
			return 0, 0, err
		}
	} else { // 将图片插入数据库
		stmt, err := tx.Prepare("INSERT INTO image_data(data) VALUES(?)")
		if err != nil {
			slog.Error(err.Error())
			return 0, 0, err
		}
		res, err := stmt.Exec(img)
		if err != nil {
			slog.Error(err.Error())
			tx.Rollback() // 如果插入失败，回滚事务
			return 0, 0, err
		}
		dataId, _ = res.LastInsertId()
	}
	//这里不提交会出现问题，原因未知
	tx.Commit()
	tx, err = db.Begin()
	if err != nil {
		slog.Error(err.Error())
		return 0, 0, err
	}
	// 将图片、MD5和预览图插入数据库
	stmt, err = tx.Prepare("INSERT INTO image_info(img_id, md5, assess_id, user_id) VALUES(?,?,?,?)")
	if err != nil {
		slog.Error(err.Error())
		tx.Rollback()
		return 0, 0, err
	}
	res, err := stmt.Exec(dataId, imgMd5, assessId, userId)
	if err != nil {
		slog.Error(err.Error())
		tx.Rollback() // 如果插入失败，回滚事务
		return 0, 0, err
	}
	id, err := res.LastInsertId()
	if err != nil {
		slog.Error(err.Error())
		tx.Rollback() // 如果获取ID失败，回滚事务
		return 0, 0, err
	}

	err = tx.Commit() // 提交事务
	if err != nil {
		slog.Error(err.Error())
		return 0, 0, err
	}

	return id, dataId, nil
}

func GetPublicImg(imageId int) (data []byte, err error) {
	db := GetDb()
	defer db.Close()

	stmt, err := db.Prepare("SELECT data FROM image_data WHERE id = ?")
	if err != nil {
		slog.Error(err.Error())
		return nil, err
	}
	rows, err := stmt.Query(imageId)
	if err != nil {
		slog.Error(err.Error())
		return nil, err
	}
	if rows.Next() {
		err = rows.Scan(&data)
		if err != nil {
			slog.Error(err.Error())
			return nil, err
		}
	} else {
		return nil, err
	}
	return data, nil
}

func GetPublicImgInfo(imageInfoId int) (userId int, assessId int, imgId int, createTime string, err error) {
	db := GetDb()
	defer db.Close()

	stmt, err := db.Prepare("SELECT user_id, assess_id,img_id,create_time FROM image_info WHERE id = ?")
	if err != nil {
		slog.Error(err.Error())
		return 0, 0, 0, "", err
	}
	rows, err := stmt.Query(imageInfoId)
	if err != nil {
		slog.Error(err.Error())
		return 0, 0, 0, "", err
	}
	if rows.Next() {
		err = rows.Scan(&userId, &assessId, &imgId, &createTime)
		if err != nil {
			slog.Error(err.Error())
			return 0, 0, 0, "", err
		}
	} else {
		return 0, 0, 0, "", err
	}
	return userId, assessId, imgId, createTime, nil
}
