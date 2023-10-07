create or replace table assess
(
    ID         int auto_increment
        primary key,
    user_id    int          null,
    score      decimal      null,
    comment    varchar(512) not null,
    createtime datetime     null,
    lastaccess datetime     null
);

create or replace table image_data
(
    ID   int auto_increment
        primary key,
    data blob null
);

create or replace table user
(
    ID           int auto_increment
        primary key,
    name         varchar(32)                not null,
    nickname     varchar(32) default `name` not null,
    phone        varchar(11) default ''     not null,
    email        varchar(128)               not null,
    portrait     mediumblob  default ''     not null,
    gender       char        default 'U'    not null,
    password     varchar(128)               null comment 'salted',
    logintime    datetime                   not null,
    loginaddress varchar(128)               not null,
    exittime     datetime                   not null,
    allowlogin   tinyint(1)                 not null
);

create or replace table image_info
(
    ID        int auto_increment
        primary key,
    img_id    int          not null,
    preview   blob         not null,
    user_id   int          null,
    assess_id int          null,
    md5       varchar(128) null,
    constraint image_info_pk
        unique (md5),
    constraint image_info_assess_ID_fk
        foreign key (assess_id) references assess (ID),
    constraint image_info_image_data_ID_fk
        foreign key (img_id) references image_data (ID),
    constraint image_info_user_ID_fk
        foreign key (user_id) references user (ID)
);
