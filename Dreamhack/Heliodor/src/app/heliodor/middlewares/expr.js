const path = require('path');

/* Resolve jq expression into an absolute path. */
function jq2path(expr) {
  return path.resolve('/tmp/jsonfs/', expr.split('.').slice(1).join('/'));
}

/* Check single jq expression and save it to req.exprPath. */
function checkExprOne(req, res, next) {
  const expr = req.params.expr;
  if (
    typeof expr !== 'string' ||
    !/^(\.[0-9A-Za-z_-]*)+$/.test(expr)
  ) {
    const err = new Error("Invalid JSON query expression.");
    err.status = 400;
    return next(err);
  } else {
    req.exprPath = jq2path(expr);
    return next();
  }
}

/* Check multiple jq expressions and save it to req.exprPaths. */
function checkExprMany(req, res, next) {
  const expr = req.params.expr;
  if (
    typeof expr !== 'string' ||
    !/^(\.[0-9A-Za-z_-]*)+(,(\.[0-9A-Za-z_-]*)+)*$/.test(expr)
  ) {
    const err = new Error("Invalid JSON query expression.");
    err.status = 400;
    return next(err);
  } else {
    const exprs = expr.split(',');
    req.exprPaths = exprs.map(jq2path);
    return next();
  }
}

module.exports = { checkExprOne, checkExprMany };
