const express = require('express');
const fs = require('fs');
const { checkExprOne, checkExprMany } = require('../middlewares/expr');
const router = express.Router();

/* GET single value. */
router.get('/view/:expr', checkExprOne, function(req, res, next) {
  return res.download(req.exprPath, function(err) {
    if (err && !res.headersSent) {
      err.status = 500;
      return next(err);
    }
  });
});

/* GET multiple key listings. */
router.get('/list/:expr', checkExprMany, function(req, res, next) {
  const done = (function() {
    const keyLists = new Array(req.exprPaths.length);
    let count = 0;
    return function(idx, keysOrError) {
      keyLists[idx] = keysOrError;
      if (++count === keyLists.length) {
        return res.json(keyLists);
      }
    };
  })();
  req.exprPaths.forEach(function(expr, idx) {
    fs.readdir(expr, function(err, files) {
      return done(idx, err || files);
    });
  });
});

module.exports = router;
