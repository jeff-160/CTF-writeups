const crypto = require('crypto');
const puppeteer = require('puppeteer');

const FLAG = process.env.FLAG || 'DH{fake_flag}';


const generateMD5Hash = (random) => {
    return crypto.createHash('md5').update(random).digest('hex');
}

const sleep = (time) => {
    return new Promise(resolve => {
      setTimeout(resolve, time)
    });
  }

const bot = async (path, memoId) => {
    const browser = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome-stable",
        headless: "new",
        args: ["--no-sandbox", "--disable-gpu"],
    });
    
    try {
            const page = await browser.newPage();
            const response = await page.goto('http://127.0.0.1:3000/home/' + path);
            if (response.status() !=200 ){
                await page.close();
                await browser.close();
                return false;
            }
            await sleep(1 * 1000);
            await page.setCookie({
                name: "FLAG",
                value: FLAG,
                domain: '127.0.0.1',
                path: "/",
            });
            await page.goto(`http://127.0.0.1:3000/memo/check?id=${memoId}`);
            await sleep(2 * 1000);
            await page.close();
            await browser.close();
            return true;

    }catch (e){
        console.log(`Bot Error: ${e}`);
        return false;
    }
}

module.exports={
    generateMD5Hash,
    bot
}