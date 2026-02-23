import { Database } from "bun:sqlite";

export function getDB() {
	const db = new Database(":memory:");
	db.run(`
CREATE TABLE users (
	name string UNIQUE NOT NULL,
	password string NOT NULL
);
`);
	db.run(`INSERT INTO users VALUES ('admin', '${getEnv("FLAG")}')`);
	return db;
}

function getEnv(name: string) {
	const e = process.env[name];
	if (!e) throw new Error(`env var not found: ${name}`);
	return e;
}
