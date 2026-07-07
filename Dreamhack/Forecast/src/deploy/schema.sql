-- Forecast Analytics: shared schema for the public API and admin console.

CREATE TABLE IF NOT EXISTS accounts (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    email         VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('customer','operator') NOT NULL DEFAULT 'customer',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    token       VARCHAR(128) PRIMARY KEY,
    account_id  INT NOT NULL,
    expires_at  TIMESTAMP NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS report_jobs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    account_id  INT NOT NULL,
    status      VARCHAR(32) NOT NULL DEFAULT 'queued',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (email, password_hash, role)
VALUES ('release-bot@forecast.internal',
        '$2b$12$h0z6t0u3pZQqVdQ5G0fE3.YH4kXcK0pNqI3qS7HhTzAv4kEoMfQ3y',
        'operator');
