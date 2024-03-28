package com.kyliancc.mozhiback.repository;

import com.kyliancc.mozhiback.model.Assessment;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;

@Mapper
@Repository
public interface AssessMapper {
    @Insert("insert into inkin.assess (user_id, image_data, score, comment, char_name, upload_date)" +
            "values (#{userId}, #{imageData}, #{score}, #{comment}, #{charName}, current_date())")
    void insertAssess(@Param("userId") int userId,
                      @Param("imageData") String imageData,
                      @Param("score") float score,
                      @Param("comment") String comment,
                      @Param("charName") String charName);

    @Delete("delete from inkin.assess where id = #{id}")
    void deleteAssess(int id);

    @Delete("delete from inkin.assess where create_date < #{date}")
    void deleteBefore(Date date);

    @Select("select score, comment, char_name from inkin.assess where id = #{id}")
    Assessment queryById(int id);

    @Select("select image_data from inkin.assess where id = #{id}")
    String queryImageDataById(int id);

    @Select("select last_insert_id()")
    int getLastInsertId();

    @Select("select id, score, comment, char_name as charName, upload_date as uploadDate from inkin.assess where user_id = #{userId}")
    List<Assessment> queryIdByUserId(int userId);

    @Select("select score, comment, char_name as charName from inkin.assess where (id = #{id}, user_id = #{userId})")
    Assessment queryByDoubleId(@Param("id") int id, @Param("userId") int userId);
}
