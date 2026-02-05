import express from 'express';
import { clone } from '../utils/merge';

const router = express.Router();

router.use((req, res, next) => {
  if (req.username !== 'admin') { 
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
});

router.get('/', (req, res) => {
  return res.render('admin');
}); 

router.post('/', async (req, res) => {
  try {
    const body = JSON.stringify(req.body).toLowerCase();

    const keywords = ['flag', 'app', '+', ' ', 'join', '!', '[', ']', '$', '_', '`', 'global', 'this', 'return', 'fs', 'child', 'eval', 'object', 'buffer', 'from', 'atob', 'btoa', '\\x', '\\u', '%']; //TODO: add more keywords. process, binding, etc.
  
    const result = keywords.filter(keyword => body.includes(keyword));
    if (result.length > 0) {
        if (
          !result.includes(' ') ||
          (result.includes(' ') && result.length > 1) ||
          (result.includes(' ') &&
            result.length === 1 &&
            body.split(' ').length !== 2)
        ) {
            return res.status(400).json({ error: 'Filtered! - ' + result.join(', ') });
        }
    }
  
    const data = clone(req.body);
    return res.json(data);
  } catch (e) {
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router;
