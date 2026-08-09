const path = require("path");
const { spawn } = require("child_process");

function createBot({ timeout = 20000 }) {
  async function run(url) {
    await new Promise((resolve) => {
      const env = {
        ...process.env,
        TIMEOUT: String(timeout),
      };

      const child = spawn(process.env.PYTHON || "python3", [path.join(__dirname, "bot.py"), url], {
        cwd: __dirname,
        env,
        stdio: "ignore",
      });

      child.on("error", (error) => {
        resolve();
      });

      child.on("exit", () => {
        resolve();
      });
    });
  }

  async function enqueue(url) {
    await run(url);
  }

  return { enqueue };
}

module.exports = { createBot };
