package com.kyliancc.mozhiback.model;

import java.util.Date;

public class User {
    private int id;
    private int token;
    private Date createDate;
    private Date lastActive;

    public User() {}

    public User(int id, int token, Date createDate, Date lastActive) {
        this.id = id;
        this.token = token;
        this.createDate = createDate;
        this.lastActive = lastActive;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getToken() {
        return token;
    }

    public void setToken(int token) {
        this.token = token;
    }

    public Date getCreateDate() {
        return createDate;
    }

    public void setCreateDate(Date createDate) {
        this.createDate = createDate;
    }

    public Date getLastActive() {
        return lastActive;
    }

    public void setLastActive(Date lastActive) {
        this.lastActive = lastActive;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", token=" + token +
                ", createDate=" + createDate +
                ", lastActive=" + lastActive +
                '}';
    }
}
