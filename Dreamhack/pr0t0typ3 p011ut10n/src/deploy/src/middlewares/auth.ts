import { NextFunction, Request, Response } from 'express';
import { verify } from '../utils/jwt';

export function authenticateToken(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
  
    if (!token) return res.status(401).json({ error: 'Unauthorized' });
  
    const t = verify(token);
    if (t) {
      req.username = t.username;
      next();
    } else {
      res.status(403).json({ error: 'Forbidden' });
    }
  } catch (e) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
