const { sign, verify } = require('../utils/jwt');

const auth = async (req, res, next) => {
    try {
        if (req.cookies.jwt === undefined) {
            let token = await sign();
            res.cookie('jwt', token, { maxAge: 3600000 });
            return res.send("You are not admin").status(401);
        }
        
        const TOKEN = req.cookies.jwt;
        const { role } = verify(TOKEN);
        if (role !== null && role ==="admin"){
            return next();
        }else{
            return res.send("You are not admin").status(401);
        }


    } catch (error) {
        console.log(`[-] auth error : ${error}`);
        return res.send("You need to generate proper jwt").status(500);
    }
}

module.exports = {
    auth
}   