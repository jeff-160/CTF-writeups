import puppeteer from "puppeteer";
import { adminCookie } from "./app.js";

export const report = async (endpoint) => {
	if (!endpoint.startsWith("?src=")) {
		throw new Error(
			"Invalid endpoint. Make sure to have the '?src=' query parameter."
		);
	}

	const browser = await puppeteer.launch({
		headless: "new",
		args: [
			"--disable-gpu",
			"--no-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		],
		executablePath: "/usr/bin/chromium-browser",
	});

	const page = await browser.newPage();
	await page.setCookie({
		name: "admin",
		value: adminCookie,
		domain: "localhost",
		path: "/",
		//httpOnly: true,
	});

	await page.goto(`http://localhost:3000/${endpoint}`);

	await new Promise((resolve) => setTimeout(resolve, 1000));

	await browser.close();
};
