const path = require('path');

/* Recursively sanitize and linearize given object. */
function sanitizeObject(obj, dir, deltas) {
  if (typeof obj === 'string') {
    deltas.push({type: 'file', dir: dir, data: obj});
    return true;  // String => file, safe
  } else if (typeof obj === 'object') {
    // Object keys => directory, regex check
    // Object values => directory/file, recursively check
    deltas.push({type: 'dir', dir: dir});
    return Object.keys(obj).every(function(k) {
      return /^[0-9A-Za-z_-]*$/.test(k) &&
             sanitizeObject(obj[k], path.resolve(dir, k), deltas);
    });
  } else {
    return false;  // Unexpected type, unsafe
  }
}

/* Sanitize JSON input and linearize into filesystem operations. */
function sanitizeBody(req, res, next) {
  deltas = []
  if (
    typeof req.body !== 'object' ||
    !sanitizeObject(req.body, '/tmp/jsonfs/', deltas)
  ) {
    const err = new Error("Invalid or unsafe JSON.");
    err.status = 400;
    return next(err);
  }
  req.deltas = deltas.reverse();
  return next();
}

module.exports = sanitizeBody
