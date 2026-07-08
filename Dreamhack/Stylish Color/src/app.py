from flask import Flask, render_template, request, redirect, url_for, abort, flash
from bs4 import BeautifulSoup
import html
import os
from pathlib import Path
import soupsieve as sv
import tinycss2

app = Flask(__name__)
app.secret_key = os.urandom(16)

reports = []

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
FLAG_PATH = Path(PROJECT_ROOT) / "private" / "flag.txt"
DEFAULT_ORACLE_COLOR = "rgb(128, 0, 0)"
ALLOWED_PROPERTIES = {"background", "background-color"}


def read_flag() -> str:
    return FLAG_PATH.read_text(encoding="utf-8").strip()


def build_hidden_page(flag_value: str) -> BeautifulSoup:
    markup = f"""
    <div class="panel">
        <input id="flag" type="password" value="{html.escape(flag_value, quote=True)}" readonly>
        <div id="oracle"></div>
    </div>
    """
    return BeautifulSoup(markup, "html.parser")


def apply_css(css: str, flag_value: str) -> dict[str, str]:
    soup = build_hidden_page(flag_value)
    oracle = soup.select_one("#oracle")
    if oracle is None:
        return {"status": DEFAULT_ORACLE_COLOR, "error": "Oracle target is missing."}

    current_color = DEFAULT_ORACLE_COLOR

    try:
        rules = tinycss2.parse_stylesheet(
            css,
            skip_comments=True,
            skip_whitespace=True,
        )
    except Exception:
        return {"status": DEFAULT_ORACLE_COLOR, "error": "Invalid CSS."}

    for rule in rules:
        if rule.type != "qualified-rule" or rule.content is None:
            continue

        selector = tinycss2.serialize(rule.prelude).strip()
        if not selector:
            continue

        try:
            matches = sv.match(selector, oracle)
        except Exception:
            return {
                "status": DEFAULT_ORACLE_COLOR,
                "error": f"Unsupported selector: {selector}",
            }

        if not matches:
            continue

        declarations = tinycss2.parse_declaration_list(
            rule.content,
            skip_comments=True,
            skip_whitespace=True,
        )
        for declaration in declarations:
            if declaration.type != "declaration":
                continue

            if declaration.lower_name not in ALLOWED_PROPERTIES:
                continue

            value = tinycss2.serialize(declaration.value).strip()
            if value:
                current_color = value

    return {"status": current_color, "error": ""}


def run_oracle(css: str) -> dict[str, str]:
    return apply_css(css, read_flag())


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", reports=reports)


@app.route("/submit", methods=["POST"])
def submit():
    css = request.form.get("css", "")

    if not css:
        flash("CSS is required.")
        return redirect(url_for("index"))

    if len(css) > 5000:
        flash("CSS is too long.")
        return redirect(url_for("index"))

    oracle = run_oracle(css)
    reports.append(
        {
            "css": css,
            "status": oracle["status"],
            "error": oracle["error"],
        }
    )
    idx = len(reports) - 1
    return redirect(url_for("view_report", idx=idx))


@app.route("/view/<int:idx>", methods=["GET"])
def view_report(idx: int):
    if idx < 0 or idx >= len(reports):
        abort(404)

    return render_template(
        "report_view.html",
        report=reports[idx],
        idx=idx,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
