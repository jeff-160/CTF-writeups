import time
import os
from uuid import UUID
from flask import Flask, render_template, request, redirect, url_for, abort
from utils import set_attr
from models import Memo

def get_memo_with_auth_or_abort(memo_id: str, password: str) -> Memo:
    memo = Memo.get_memo_by_id(memo_id)

    if memo is None:
        abort(404)
    elif not memo.check_password(password):
        abort(403)

    return memo


secret = Memo("secret", open("/flag", "r").read(), os.urandom(20).hex())

Memo.add_memo_to_collection(secret)

app = Flask(__name__)


@app.route("/")
def index():
    memo_title_list = [
        (memo.id, memo.get_title()) for memo in Memo.collections.values()
    ]

    return render_template("index.html", memos=memo_title_list)


@app.route("/new", methods=["GET", "POST"])
def new_memo():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        password = request.form["password"]

        Memo.add_memo_to_collection(Memo(title, content, password))

        return redirect(url_for("index"))
    return render_template("new_memo.html")


@app.route("/edit/<uuid:memo_id>", methods=["GET", "POST"])
def edit_memo(memo_id: UUID):
    memo_id = str(memo_id)

    if request.method == "GET":
        return render_template("edit_memo.html", memo_id=memo_id)
    elif request.method == "POST":
        selected_option = request.form["selected_option"]
        edit_data = request.form["edit_data"]
        password = request.form["password"]

        memo = get_memo_with_auth_or_abort(memo_id, password)

        set_attr(memo, selected_option + ".data", edit_data)
        set_attr(memo, selected_option + ".edit_time", time.time())

        return redirect(url_for("index"))


@app.route("/view/<uuid:memo_id>", methods=["GET", "POST"])
def view_memo(memo_id: UUID):
    memo_id = str(memo_id)

    if request.method == "GET":
        return render_template("enter_password.html", memo_id=memo_id)
    elif request.method == "POST":
        password = request.form["password"]

        memo = get_memo_with_auth_or_abort(memo_id, password)

        contents = (
            memo.get_title_with_edit_time() + "\n" + memo.get_content_with_edit_time()
        )

        return render_template("view_memo.html", memo=contents, memo_id=memo_id)


if __name__ == "__main__":
    app.run(debug=False)
