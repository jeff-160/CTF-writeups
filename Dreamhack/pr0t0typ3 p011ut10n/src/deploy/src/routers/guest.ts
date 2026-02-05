import express from 'express';

const router = express.Router();

router.get('/', (req, res) => {
  return res.send(`Hello ${req.username}`);
});

export default router;
