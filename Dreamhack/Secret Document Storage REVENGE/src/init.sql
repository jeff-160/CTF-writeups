
-- 데이터베이스 생성 및 사용
CREATE DATABASE IF NOT EXISTS document;
USE document;

-- document 테이블 생성
CREATE TABLE IF NOT EXISTS document (
    title VARCHAR(255),
    content VARCHAR(1000),
    filename VARCHAR(255)
);

-- secret 테이블 생성
CREATE TABLE IF NOT EXISTS secret (
    secret_data VARCHAR(255) NOT NULL
);

-- document 테이블에 데이터 삽입
INSERT INTO document (title, content, filename)
VALUES ('TOP SECRET DOCUMENT', 'REDACTED', '655f365d59872.png');

-- secret 테이블에 데이터 삽입
INSERT INTO secret (secret_data)
VALUES ('REDACTED');

CREATE USER 'fake'@'%' IDENTIFIED BY 'fake';
GRANT ALL PRIVILEGES ON *.* TO 'fake'@'%';
FLUSH PRIVILEGES;
