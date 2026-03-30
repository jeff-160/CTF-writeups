const router = require('express').Router();
const { auth } = require("../middleware/auth");
const { getBalance } = require('../utils/balance');

const FLAG = process.env.FLAG || "DH{**fake_flag**}"

router.get("/", auth, (req,res)=>{
    if (getBalance() >= 10){
        
        return res.send(FLAG);
    }
    else{
        return res.send("Insufficient balance");
    }
})

router.post("/", auth, (req, res) => {
    res.send("Hi guest");
})

module.exports=router