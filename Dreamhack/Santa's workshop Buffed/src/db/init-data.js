const crypto = require('crypto');
var conn = new Mongo();

var db = conn.getDB('nest');

db.users.insertMany([
  { username: 'admin', password: crypto.randomBytes(16).toString('hex') },
]);


db.flags.insertMany([
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
  { name: 'TEST', user: "" },
]);
