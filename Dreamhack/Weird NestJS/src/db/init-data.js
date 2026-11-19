const crypto = require('crypto');
var conn = new Mongo();

var db = conn.getDB('nest');

db.users.insertMany([
  { id: 'guest', password: crypto.randomBytes(16).toString('hex') },
  { id: 'admin', password: crypto.randomBytes(16).toString('hex') },
]);