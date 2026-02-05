import mysql, { RowDataPacket } from 'mysql2/promise';
import crypto from 'crypto';

let db: mysql.Connection | null = null;

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
export async function getDB() {
  if (db) return db;

  console.info('Connecting to database...');
  await sleep(10000);

  const connection = await mysql.createConnection({
    host: 'db',
    user: 'root',
    database: 'test',
    password: 'password',
  });

  try {
    await connection.query('DROP TABLE IF EXISTS users');
    await connection.query(
      'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)',
    );
    await connection.query('DELETE FROM users');
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['admin', crypto.randomBytes(32).toString('hex')],
    );
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['guest', 'guest'],
    );
    await connection.query(
      `INSERT INTO users (username, password) VALUES (?, ?)`,
      ['dream', 'hack'],
    );
  } catch (e) {
    console.error(e);
  }

  db = connection;

  return db;
}

export interface User extends RowDataPacket {
  id: number;
  username: string;
  password: string;
}
