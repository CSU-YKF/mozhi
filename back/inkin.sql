CREATE DATABASE IF NOT EXISTS inkin;

CREATE TABLE IF NOT EXISTS inkin.assess(
    id          int             auto_increment primary key,
    user_id     int             not null,
    image_data  text            not null,
    score       decimal(2, 1)   not null,
    comment     varchar(512)    not null,
    char_name   char(1)         not null,
    upload_date date            not null
);

CREATE TABLE IF NOT EXISTS inkin.user(
    id          int     auto_increment primary key,
    token       int     not null,
    create_date date    not null,
    last_active date    not null
);