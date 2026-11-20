import express from "express";

import { visit } from "./bot.mjs";

const PORT = "31337";

const app = express();
app.use(express.json());

app.use(express.static("public"));

app.post("/visit", async (req, res) => {
  try {
    const url = req.body.url;
    console.log(req.body);
    await visit(url);
    return res.sendStatus(200);
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

app.listen(PORT);