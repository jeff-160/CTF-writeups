import express from "express";
import rateLimit from "express-rate-limit";

import { visit, APP_URL } from "./bot.mjs";

const PORT = "1337";

const app = express();
app.use(express.json());

app.use(express.static("public"));

app.get("/app-url", async (req, res) => {
  return res.send(APP_URL);
});

app.use(
  "/api",
  rateLimit({
    // Limit each IP to 4 requests per 1 minute
    windowMs: 60 * 1000,
    max: 4,
  })
);

app.post("/api/report", async (req, res) => {
  const { path } = req.body;
  try {
    await visit(path);
    return res.sendStatus(200);
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

app.listen(PORT);