CREATE DATABASE IF NOT EXISTS inkin;

CREATE TABLE IF NOT EXISTS inkin.assess
(
    ID         int auto_increment
        primary key,
    user_id    int          null,
    score      decimal      null,
    comment    varchar(512) not null,
    createtime datetime     null default now(),
    lastaccess datetime     null
);

CREATE TABLE IF NOT EXISTS inkin.image_data
(
    ID   int auto_increment
        primary key,
    data LONGBLOB null
);

CREATE TABLE IF NOT EXISTS inkin.user
(
    ID           int auto_increment
        primary key,
    name         varchar(32)                not null,
    nickname     varchar(32) default 'default' not null,
    phone        varchar(11) default '0'     not null,
    email        varchar(128)               not null,
    portrait     mediumblob  not null,
    gender       char        default 'U'    not null,
    saltpassword varchar(128)               null comment 'salted',
    logintime    datetime                   not null,
    loginaddress varchar(128)               not null,
    exittime     datetime                   not null,
    allowlogin   tinyint(1)                 not null,
    salt         char(16)                   not null
);

CREATE TABLE IF NOT EXISTS inkin.image_info
(
    ID        int auto_increment
        primary key,
    img_id    int          not null,
    user_id   int          null comment 'the user who upload the image, 如果user_id为0，then it is a public image',
    assess_id int          null ,
    md5       varchar(128) null,
    create_time datetime     not null default now()
);