const createError = require('http-errors');
const express = require('express');
const logger = require('morgan');

const queryRouter = require('./routes/query');
const updateRouter = require('./routes/update');

const app = express();

if (process.env.NODE_ENV === 'development') {
  app.use(logger('dev'));
}
app.use(express.json());

app.get('/', function(req, res, next) {
  return res.redirect('/query/list/%2e');
});
app.use('/query', queryRouter);
app.use('/update', updateRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set error info, only providing stacktrace in development
  const errinfo = {};
  errinfo.message = err.message;
  errinfo.error =
    req.app.get('env') === 'development' ?
    {status: err.status, stack: err.stack} : {};

  // render the error page
  res.status(err.status || 500);
  res.json(errinfo);
});

module.exports = app;
