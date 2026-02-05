import express from 'express';
import { getDB, User } from '../db';
import { FieldPacket } from 'mysql2';
import { sign } from '../utils/jwt';

const router = express.Router();

//* prototype pollution을 한 번 시도한 이후에는 login 시도시 Internal Server Error가 발생할 수 있으니, token을 저장해주세요.

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ error: 'Invalid input' });
    }
  
    const db = await getDB();
  
    const [rows, fields]: [User[], FieldPacket[]] = await db.query(
      'SELECT * FROM users WHERE username = ? and password = ? LIMIT 1',
      [username, password],
    );
  
    if (rows.length !== 1) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
  
    const token = sign({ username: rows[0].username, password: rows[0].password });
    return res.json({ token });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: 'Internal Server Error.' });
  }
});

router.post('/register', async (req, res) => {
  try {
    const { username, password } = req.body;
    if (
      !username ||
      !password ||
      typeof username !== 'string' ||
      typeof password !== 'string' ||
      username.toLowerCase() === 'admin'
    ) {
      return res.status(400).json({ error: 'Invalid input' });
    }
  
    const db = await getDB();
  
    try {
      await db.execute('INSERT INTO users (username, password) VALUES (?, ?)', [
        username.toLowerCase(),
        password,
      ]);
      return res.status(201).json({ username: username.toLowerCase() });
    } catch (e) {
      return res.status(409).json({ error: 'User already exists' });
    }
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: 'Internal Server Error.' });
  }
});

export default router;
