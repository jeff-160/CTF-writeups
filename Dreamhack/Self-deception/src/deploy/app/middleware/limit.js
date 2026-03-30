const { setBalance } = require('../utils/balance');

const chargeCount = {};

const limitCharge = (req, res, next) => {
  const ip = req.ip;
  console.log(`[+] ip ==> ${ip}`)
  if (!chargeCount[ip]) {
    chargeCount[ip] = 1;
  } else {
    chargeCount[ip]++;
  }

  if (chargeCount[ip] >= 3) {
    setBalance(1);
    chargeCount[ip] = 0;
    console.log(`[+] balance reset`);
    return res.status(429).send("Exceeded today's charge limit");
  }

  next();
};


module.exports = {
    limitCharge
}   