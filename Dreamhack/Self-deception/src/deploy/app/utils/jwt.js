const fs = require('fs');
const { createSigner, createVerifier } = require('fast-jwt');

const sign = async() => {
    try {
        const KEY = fs.readFileSync("./key/private.pem","utf-8");
        const payload = { role: "guest" };
        const signSync = createSigner({ algorithm: 'RS256', key: KEY });
        const token = signSync(payload);
        return token;
        
    } catch (error){
        console.log(`[-] sign error ${error}`)
        return null;
    }

}

const verify = (token) => {
    try{
        const KEY = fs.readFileSync("./key/public.pem","utf-8");
        const verifySync = createVerifier({ key: KEY });
        const payload = verifySync(token);
        return payload;
    } catch (error){
        console.log(`[-] verify error ${error}`)
        return null;
    }

}

module.exports = {
    sign,
    verify
}