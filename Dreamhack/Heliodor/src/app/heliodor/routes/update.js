const express = require('express');
const fs = require('fs');
const sanitizeBody = require('../middlewares/sanitize-body');
const router = express.Router();

/* POST JSON value into filesystem. */
router.post('/patch', sanitizeBody, function(req, res, next) {
  function commitDeltas(err) {
    if (err) {
      err.status = 500;
      return next(err);
    } else if (req.deltas.length === 0) {
      return res.json({success: true});
    } else {
      const delta = req.deltas.pop();
      if (delta.type === 'file') {
        return fs.writeFile(delta.dir, delta.data, commitDeltas);
      } else {  // delta.type === 'dir'
        return fs.mkdir(delta.dir, function(err) {
          return commitDeltas(err?.code === 'EEXIST' ? null : err);
        });
      }
    }
  }
  commitDeltas(null);
});

/* POST to reset jsonfs. */
router.post('/reset', function(req, res, next) {
  // Remove the whole jsonfs directory, and then reconstruct.
  fs.rm('/tmp/jsonfs', {recursive: true, force: true}, function(err_rm) {
    // Regardless of error, recreate jsonfs directory.
    fs.mkdir('/tmp/jsonfs', function(err_mkdir) {
      const result = {success: !err_rm && !err_mkdir, err_rm, err_mkdir}
      return res.status(result.success ? 200 : 500).json(result);
    });
  });
});

module.exports = router;
