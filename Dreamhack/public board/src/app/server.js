const path = require("path");

const cookieSession = require("cookie-session");
const express = require("express");

const { createBot } = require("./bot");

const app = express();

const port = Number.parseInt(process.env.PORT || "3000", 10);
const secret = process.env.SECRET || "redacted";
const timeout = Number.parseInt(process.env.TIMEOUT || "20000", 10);
const origins = (process.env.ORIGINS ||
  `http://localhost:${port},http://127.0.0.1:${port}`)
  .split(",")
  .map((value) => value.trim())
  .filter(Boolean);

const users = new Map();
const posts = [];
let nextId = 1;

function userOf(req) {
  const name = req.session?.username;
  if (!name || !users.has(name)) {
    return null;
  }

  return users.get(name);
}

function noteOf(req) {
  return typeof req.query.note === "string" ? req.query.note : "";
}

function view(req, data = {}) {
  return {
    user: userOf(req),
    note: noteOf(req),
    ...data,
  };
}

function go(res, url, note = "") {
  if (!note) {
    res.redirect(url);
    return;
  }

  const query = new URLSearchParams({ note }).toString();
  res.redirect(`${url}?${query}`);
}

function needUser(req, res, next) {
  const user = userOf(req);
  if (!user) {
    go(res, "/login", "Login required");
    return;
  }

  req.user = user;
  next();
}

function normalize(raw) {
  const parsed = new URL(raw);
  if (!origins.includes(parsed.origin)) {
    throw new Error("nope");
  }

  return `http://127.0.0.1:${port}${parsed.pathname}${parsed.search}${parsed.hash}`;
}

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: false }));
app.use(
  cookieSession({
    name: "session",
    keys: [secret],
    httpOnly: true,
    sameSite: "lax",
  }),
);
app.use("/static", express.static(path.join(__dirname, "public")));

const bot = createBot({ timeout });

app.get("/", (req, res) => {
  res.render(
    "index",
    view(req, {
      title: "Post List",
      posts,
    }),
  );
});

app.get("/register", (req, res) => {
  res.render(
    "register",
    view(req, {
      title: "Register",
    }),
  );
});

app.post("/register", (req, res) => {
  const username = String(req.body.username || "").trim();
  const password = String(req.body.password || "");

  if (username.length < 3 || password.length < 3) {
    go(res, "/register", "Invalid input");
    return;
  }

  if (users.has(username)) {
    go(res, "/register", "Username already exists");
    return;
  }

  users.set(username, { username, password });
  res.redirect("/login");
});

app.get("/login", (req, res) => {
  res.render(
    "login",
    view(req, {
      title: "Login",
    }),
  );
});

app.post("/login", (req, res) => {
  const username = String(req.body.username || "").trim();
  const password = String(req.body.password || "");
  const user = users.get(username);

  if (!user || user.password !== password) {
    go(res, "/login", "Invalid credentials");
    return;
  }

  req.session.username = user.username;
  res.redirect("/");
});

app.get("/logout", (req, res) => {
  req.session = null;
  res.redirect("/");
});

app.get("/write", needUser, (req, res) => {
  res.render(
    "write",
    view(req, {
      title: "Write",
    }),
  );
});

app.post("/write", needUser, (req, res) => {
  const title = String(req.body.title || "").trim();
  const content = String(req.body.content || "");

  if (!title || !content) {
    go(res, "/write", "Invalid input");
    return;
  }

  const post = {
    id: nextId++,
    title,
    content,
    author: req.user.username,
  };

  posts.push(post);
  res.redirect(`/posts/${post.id}`);
});

app.get("/posts/:id", (req, res) => {
  const id = Number.parseInt(req.params.id, 10);
  const post = posts.find((item) => item.id === id);

  if (!post) {
    res.status(404).render(
      "missing",
      view(req, {
        title: "Not Found",
      }),
    );
    return;
  }

  res.render(
    "post",
    view(req, {
      title: post.title,
      post,
    }),
  );
});

app.get("/report", needUser, (req, res) => {
  res.render(
    "report",
    view(req, {
      title: "Report",
      url: origins[0] || "",
    }),
  );
});

app.post("/report", needUser, (req, res) => {
  const raw = String(req.body.url || "").trim();

  try {
    const url = normalize(raw);
    void bot.enqueue(url);
    go(res, "/report", "Report queued");
  } catch (error) {
    go(res, "/report", error.message);
  }
});

app.listen(port);
