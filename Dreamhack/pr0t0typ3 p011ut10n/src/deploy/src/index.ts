import express, { ErrorRequestHandler } from 'express';
import path from 'path';
import { authenticateToken } from './middlewares/auth';
import admin from './routers/admin';
import guest from './routers/guest';
import auth from './routers/auth';
import { getDB } from './db';
 
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(import.meta.dirname, '../views'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.render('index');
});

app.use('/admin', authenticateToken, admin);
app.use('/guest', authenticateToken, guest);
app.use('/auth', auth);

app.use(((err, req, res, next) => {
  console.error(err);
  const status = err.status ?? 500;
  return res.status(status).json({
    message: err.message,
    status,
  });
}) as ErrorRequestHandler);

app.listen(3000, '0.0.0.0', () => {
  console.log('Server is running on http://0.0.0.0:3000');
});

await getDB();

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception thrown', err);
});