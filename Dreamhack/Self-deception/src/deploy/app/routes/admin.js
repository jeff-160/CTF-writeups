const router = require('express').Router();
const { auth } = require("../middleware/auth");
const { limitCharge } = require("../middleware/limit");
const { getBalance, setBalance } = require('../utils/balance');

const isValidDecimal = (num) => {
    const regex = /^0\.\d+$/;
    return regex.test(num);
}

router.get("/", (req,res)=>{
    res.send("This is admin page");
})

router.get("/charge", limitCharge, auth, (req,res)=>{
    const money = req.query.money;
    let balance = getBalance();
    if (isValidDecimal(money)){
        const op = parseFloat(money);
        setBalance(balance + op);
        console.log(`[+] balance ==> ${getBalance()}`)
        
        return res.send("OK");
    }
    else{
        console.log(`[-] The money is invaild`);
        return res.send("The money is invaild");
    }
})

router.get("/withdraw", auth, (req,res)=>{
    const money = req.query.money;
    let balance = getBalance();
    let tmp = 0;
    if (isValidDecimal(money)){
        const op = parseFloat(money);
        let dollar = "";
        if (balance < op){
            TRY +=1;
            return res.send("The amount you are trying to withdraw is more than the balance");
        }
        tmp = balance - op;
        dollar = tmp + "$";
        msg = `Your balance is ${dollar}`;
        setBalance(parseInt(dollar.split("$")[0]));
        console.log(`[+] balance ==> ${getBalance()}`);

    }
    else{
        console.log(`[-] The money is invaild`);
        return res.send("The money is invaild");
    }
    return res.send(msg);
})

module.exports=router