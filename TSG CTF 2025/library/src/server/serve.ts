import express from "express";
import { getDB } from "./lib/db.ts";

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("./app"));

type QueryParams = { name?: string; password?: string };

app.get("/actions/login", (req, res) => {
	const db = getDB();

	const query: QueryParams = req.query;
	console.log("query", query);

	if (!query || !query.name || !query.password) {
		return res.status(400).send("bad parameters");
	}
	if (query.name.includes("'") || query.password.includes("'")) {
		return res.status(400).send("haha nice try");
	}

	const sql = `SELECT name FROM users WHERE name = '${query.name}' AND password = '${query.password}'`;
	console.log("sql", sql);

	const user = db.query(sql).get() as { name: string } | null;

	if (!user || !user.name) return res.status(400).send(`Staff not found`);
	return res.send(`Welcome, ${user.name}. You now have access to the restricted archives.`);
});

const port = process.env.PORT ?? "3000";
app.listen(port, () => {
	console.log(`server is listening at localhost:${port}`);
});
