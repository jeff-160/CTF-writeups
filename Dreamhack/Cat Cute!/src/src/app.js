import express from "express";
import rateLimit from "express-rate-limit";
import cookieParser from "cookie-parser";
import { randomUUID } from "crypto";
import { report } from "./bot.js";

const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 1,
  standardHeaders: true,
  legacyHeaders: false,
});

const app = express();
export const adminCookie = randomUUID();

app.set('view engine', 'ejs');
app.set("views", "templates/");

app.use(cookieParser());
app.use(express.json());
app.use('/static', express.static('static'));

app.get("/", (req, res) => {
  res.render("index", {src : req.query.src});
});

app.post("/report", limiter, async (req, res) => {
  try {
    if (!req.body.text) {
      throw new Error("Invalid input.");
    }
    if (typeof req.body.text !== "string") {
      throw new Error("Invalid input.");
    }
    await report(req.body.text);
    return res.json({ success: true });
  } catch (err) {
    return res.status(400).json({ success: false });
  }
});

app.get('/admin', (req,res) => {
  if (req.cookies?.admin === adminCookie) {
    res.render('admin', {...req.query});
  }
  else{
    return res.status(403).send("You are not Admin!");
  }
})

const port = 3000;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
