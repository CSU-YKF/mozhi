package com.kyliancc.mozhiback.model;

import java.util.Arrays;
import java.util.Date;

public class Assessment {
    private int id;
    private int userId;
    private String imageData;
    private float score;
    private String comment;
    private String charName;
    private String basicDom;
    private String meaningDom;
    private Date uploadDate;

    public Assessment() {}

    public Assessment(int id, int userId, String imageData, float score, String comment, String charName, String basicDom, String meaningDom, Date uploadDate) {
        this.id = id;
        this.userId = userId;
        this.imageData = imageData;
        this.score = score;
        this.comment = comment;
        this.charName = charName;
        this.basicDom = basicDom;
        this.meaningDom = meaningDom;
        this.uploadDate = uploadDate;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getImageData() {
        return imageData;
    }

    public void setImageData(String imageData) {
        this.imageData = imageData;
    }

    public float getScore() {
        return score;
    }

    public void setScore(float score) {
        this.score = score;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public String getCharName() {
        return charName;
    }

    public void setCharName(String charName) {
        this.charName = charName;
    }

    public String getBasicDom() {
        return basicDom;
    }

    public void setBasicDom(String basicDom) {
        this.basicDom = basicDom;
    }

    public String getMeaningDom() {
        return meaningDom;
    }

    public void setMeaningDom(String meaningDom) {
        this.meaningDom = meaningDom;
    }

    public Date getUploadDate() {
        return uploadDate;
    }

    public void setUploadDate(Date uploadDate) {
        this.uploadDate = uploadDate;
    }

    @Override
    public String toString() {
        return "Assessment{" +
                "id=" + id +
                ", userId=" + userId +
                ", imageData=" + imageData +
                ", score=" + score +
                ", comment='" + comment + '\'' +
                ", charName='" + charName + '\'' +
                ", basicDom='" + basicDom + '\'' +
                ", meaningDom='" + meaningDom + '\'' +
                ", uploadDate=" + uploadDate +
                '}';
    }
}
