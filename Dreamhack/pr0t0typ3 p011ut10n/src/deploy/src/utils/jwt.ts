import jwt from 'jsonwebtoken';
import crypto from 'crypto';

const SECRET = crypto.randomBytes(64).toString('hex');

export function sign(user: { username: string, password: string }): string {
  return jwt.sign(user, SECRET, { expiresIn: '1h', algorithm: 'HS256' });
}

export function verify(token: string): { username: string } | null {
  try {
    return jwt.verify(token, SECRET, { algorithms: ['HS256'] }) as {
      username: string;
    };
  } catch (e) {
    console.error('JWT verification failed', e);
    return null;
  }
}
