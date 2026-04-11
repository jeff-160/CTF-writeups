-- init.sql
SET time_zone = '+00:00';

-- Create DB
CREATE DATABASE IF NOT EXISTS flask_service;

USE flask_service;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(191) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(191) NOT NULL,
    token VARCHAR(191) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    used TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    KEY idx_prt_username (username),
    KEY idx_prt_expires_at (expires_at),
    KEY idx_prt_used (used)
) ENGINE=InnoDB;

INSERT INTO users (username, password_hash) VALUES ("admin", "scrypt:32768:8:1$ylMuNL1397PlcZyj$48e76cc03517b9f8fdd815728e6f407f35e5e7962f85513b8731f65bb339e9fd14c3bc1d58caa2a4a5feb1628fdbfe0458748de046503ad9431240a0612edb24");
INSERT INTO users (username, password_hash) VALUES ("guest", "scrypt:32768:8:1$dceyi7mItzF1ggiN$df6c68c92150479964fad00493bac913ae9231a138111a892ed437908d9ee7ab7121bc8be0f26e77fde0b54789b515854529187b9ff773d75a6d8042d4540fbd");