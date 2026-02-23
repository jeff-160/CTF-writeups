# server.py
import subprocess
import tempfile
import os
from flask import Flask, request, jsonify
from hexdump import hexdump 
import re 

app = Flask(__name__)

FLAG = open("/flag.txt").read().strip()

@app.route("/challenge", methods=["POST"])
def challenge():
    payload = request.json.get("payload", "")

    results = {}
    interpreters = {
        "python": ["python3", "-c", payload],
        "javascript": ["node", "-e", payload]
    }

    for lang, cmd in interpreters.items():
        try:
            BLOCKED_KEYWORDS = [
                    "require",
                    "process",
                    "child_process",
                    "Function",
                    "constructor",
                    "globalThis",
                    "module",
                    "exports",
                    "Buffer",
                    "__proto__",
                    "Reflect",
                    "Object",
                    "`",
                    "flat",
                    "map",
                    "filter",
                    "constructor",
                    "toString",
                    "call",
                    "apply",
                    "bind",
                    "new",
                    #
                    "import",
                    "open",
                    "os",
                    "system",
                    "subprocess",
                    "input",
                    "flag",
                    "console",
                    "require",
                    "__import__",
                    "__builtins__"
            ]

            BLOCK_PATTERN = re.compile(r"|".join([fr"\b{kw}\b" for kw in BLOCKED_KEYWORDS]), re.IGNORECASE)
            if BLOCK_PATTERN.search(payload):
                return jsonify({"error": "Blocked keyword detected."}), 403

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)

            output = result.stdout.decode().strip()
            if FLAG in output:
                results[lang] = f"SUCCESS"
            else:
                results[lang] = f"FAILURE"
                return  jsonify(results)
        except Exception as e:
            results[lang] = f"Error!"
            return  jsonify(results)
    else : 
        results['flag'] = FLAG 

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

