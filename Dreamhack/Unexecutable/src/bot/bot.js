const puppeteer = require('puppeteer-core');

const visit = async (url) => {
	let browser;
    try {
		browser = await puppeteer.launch({
			headless: 'new',
			executablePath: '/usr/bin/google-chrome',
			args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--js-flags=--noexpose_wasm,--jitless']
		});
		const page = await browser.newPage();
		await page.setJavaScriptEnabled(false);
		await page.goto(`http://localhost/${url}`, { timeout: 3000, waitUntil: 'domcontentloaded' });
		await page.waitForTimeout(1500);
		
        await browser.close();
        browser = null;
	} catch (err) {
        console.log('bot error', err);
    } finally {
        if (browser) await browser.close();
    }
}

if (process.argv?.length === 3)
	visit(Buffer.from(process.argv[2], 'base64').toString('utf8'));