let balance = 1;

const getBalance = () => balance;
const setBalance = (newBalance) => { balance = newBalance; };

module.exports = { getBalance, setBalance };
