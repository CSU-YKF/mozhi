package com.kyliancc.mozhiback.repository;

import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

import java.util.Date;

@Mapper
@Repository
public interface UserMapper {
    @Insert("insert into inkin.user (token, create_date, last_active) values (#{token}, current_date(), current_date());")
    void insertUser(int token);

    @Delete("delete from inkin.user where id = #{id}")
    void deleteUser(int id);

    @Delete("delete from inkin.user where last_active < #{date}")
    void deleteLastActiveBefore(Date date);

    @Update("update inkin.user set last_active = current_date() where id = #{id}")
    void updateUserLastActive(int id);

    @Select("select id from inkin.user where token = #{token}")
    Integer queryIdByToken(int id);

    @Select("select last_insert_id()")
    int getLastInsertId();
}
