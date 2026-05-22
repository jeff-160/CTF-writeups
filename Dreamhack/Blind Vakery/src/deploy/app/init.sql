SET time_zone='+09:00';
CREATE DATABASE vakery_db CHARACTER SET utf8;
CREATE USER 'vakery_user'@'localhost' IDENTIFIED BY 'vakery_password';
GRANT ALL PRIVILEGES ON vakery_db.* TO 'vakery_user'@'localhost';

USE `vakery_db`;
DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
  idx int auto_increment primary key,
  id varchar(50) not null,
  pw varchar(100) not null
);

DROP TABLE IF EXISTS `breads`;
CREATE TABLE breads (
  name varchar(100) not null primary key,
  description varchar(200) not null,
  price int not null
);

INSERT INTO users (id, pw) values ('admin', '86401d63646a3b96baaa16c3538dda026699ff55bbc942f64d14bab1a4d95718');
INSERT INTO breads (name, description, price) values
  ("Croissant", "A flaky and buttery French pastry, known for its crescent shape and layered texture.", 10),
  ("Ciabatta", "An Italian bread with a crisp crust and porous, chewy interior, perfect for sandwiches.", 20),
  ("Cream Puff", "A light, hollow pastry filled with sweet cream or custard, often dusted with powdered sugar.", 7),
  ("Baguette", "A baguette is a long, thin loaf of French bread that is characterized by a crispy crust and a chewy texture.", 12),
  ("DH{**fake_flag**}", "This is flag for you.", 10000);