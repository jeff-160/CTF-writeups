import puppeteer from "puppeteer";

const FLAG = process.env.FLAG ?? "DH{FLAG}"

const APP_HOST = "web";
const APP_PORT = "8000";
export const APP_URL = `http://${APP_HOST}:${APP_PORT}/`;

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

export const visit = async (path) => {
  console.log(`start: ${path}`);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox"],
  });

  const context = await browser.createIncognitoBrowserContext();

  try {
    const page = await context.newPage();
    await page.setCookie({
      name: "FLAG",
      value: FLAG,
      domain: APP_HOST,
      path: "/",
    });
    await page.goto(APP_URL + path);
    await sleep(5 * 1000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`end: ${path}`);
};