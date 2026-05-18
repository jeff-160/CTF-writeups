CREATE DATABASE dream_lectures_db CHARACTER SET utf8;
CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'dbpass';
GRANT ALL PRIVILEGES ON dream_lectures_db.* TO 'dbuser'@'localhost';

USE `dream_lectures_db`;
CREATE TABLE users (
  idx int auto_increment primary key,
  uid varchar(32) not null,
  upw varchar(64) not null,
  role int not null,
  UNIQUE (uid)
);

INSERT INTO users (uid, upw, role) VALUES ('admin', 'initial_passwordqwer1234', 1);

CREATE TABLE lectures (
  idx int auto_increment primary key,
  lecture_name varchar(128) not null,
  lecturer_name varchar(32) not null,
  description varchar(256) not null,
  registration_start timestamp not null,
  registration_due timestamp not null,
  lecture_start timestamp not null,
  lecture_end timestamp not null,
  UNIQUE (lecture_name)
);

INSERT INTO lectures (
    lecture_name,
    lecturer_name,
    description,
    registration_start, registration_due,
    lecture_start, lecture_end) VALUES (
    "컴퓨터 프로그래밍",
    "김언어",
    "컴퓨터 프로그래밍을 배웁니다.",
    "2019-01-01 00:00:00", "2019-05-01 23:59:59",
    "2019-05-02 16:00:00", "2019-05-02 19:00:00");

INSERT INTO lectures (
    lecture_name,
    lecturer_name,
    description,
    registration_start, registration_due,
    lecture_start, lecture_end) VALUES (
    "식물 기르기",
    "김식물",
    "식물 기르는 방법을 배웁니다.",
    "2019-08-20 00:00:00", "2019-09-01 23:59:59",
    "2019-09-02 15:00:00", "2019-09-02 18:30:00");

INSERT INTO lectures (
    lecture_name,
    lecturer_name,
    description,
    registration_start, registration_due,
    lecture_start, lecture_end) VALUES (
    "영어 교실",
    "김영어",
    "영어를 배웁니다.",
    "2020-01-20 00:00:00", "2020-02-10 23:59:59",
    "2020-02-11 14:00:00", "2020-02-11 17:00:00");

INSERT INTO lectures (
    lecture_name,
    lecturer_name,
    description,
    registration_start, registration_due,
    lecture_start, lecture_end) VALUES (
    "제과제빵",
    "김제빵",
    "빵, 과자 만드는 방법을 배웁니다.",
    "2020-11-11 00:00:00", "2034-11-10 23:59:59",
    "2034-11-11 15:00:00", "2034-11-11 17:30:00");

CREATE TABLE applications (
  idx int auto_increment primary key,
  lecture_idx int not null,
  lecture_name varchar(128) not null,
  applicant_name varchar(32) not null,
  email varchar(128) not null,
  contact varchar(128) not null,
  reason varchar(256) not null,
  is_checked boolean not null
);
