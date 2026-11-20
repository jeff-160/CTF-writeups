import puppeteer from "puppeteer";

const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

export const visit = async (visit_url) => {
  console.log(`start trigger`);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox",
      "--disable-popup-blocking",
      "--ignore-certificate-errors",
      "--disable-features=UpgradeInsecureRequests",
      "--allow-insecure-localhost",
    ],
  });
  const context = await browser.createBrowserContext();

  async function visitUrl(page, url) {
    try {
      console.log('visiting ' + url);
      page.setDefaultNavigationTimeout(10000);
      await page.goto(url);
      await sleep(5000);
    } catch (err) {
      console.error('Error in processPage:', err);
    }
  }

  try {
    const page = await context.newPage();

    await visitUrl(page, visit_url);

  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();
};
