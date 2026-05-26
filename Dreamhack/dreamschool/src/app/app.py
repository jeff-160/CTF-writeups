import os

from flask import (
    Flask,
    Response,
    render_template,
    request,
    make_response,
    redirect,
    abort,
    render_template_string,
)
from sqlalchemy import DateTime
from pytz import timezone, utc

from error import error_template
from auth import JwtAuthenticator
from forms import RegisterForm, LoginForm, PostForm
from models import db_session, User, School, Board, Post

if os.getenv("env", "production") == "development":
    from config import Development as AppConfig
else:
    from config import Production as AppConfig

app = Flask(__name__)

app.config.from_object(AppConfig)

authenticator = JwtAuthenticator(
    app.config["AUTH_PUBLIC_KEY"], app.config["AUTH_PRIVATE_KEY"]
)
app.config.pop("AUTH_PRIVATE_KEY")


@app.template_filter("strftime")
def filter_strftime(date: DateTime, f: str = None) -> str:
    return (
        utc.localize(date)
        .astimezone(timezone(app.config["TIMEZONE"]))
        .strftime("%m. %d. %H:%M" if f == "brief" else "%Y. %m. %d. %H:%M:%S")
    )


@app.template_filter("post_list_elem_content")
def filter_post_list_elem_content(s: str) -> str:
    return f"{s[:20]}{'...' if len(s) > 25 else ''}"


@app.errorhandler(404)
@authenticator.authorize(is_abort=False)
def page_not_found(user: User, school: School, e):
    btn_title, btn_link = (
        ("홈으로", "/")
        if user is None
        else (f"{user.school_name}(으)로", f"/s/{user.school_name}")
    )
    return (
        render_template_string(
            error_template("Not Found", "해당 페이지는 존재하지 않습니다.", btn_title, btn_link)
        ),
        404,
    )


@app.errorhandler(401)
@authenticator.authorize(is_abort=False)
def unauthorized(user: User, school: School, e):
    btn_title, btn_link = (
        ("홈으로", "/")
        if user is None
        else (f"{user.school_name}(으)로", f"/s/{user.school_name}")
    )
    return (
        render_template_string(
            error_template("Unauthorized", "권한이 부족합니다.", btn_title, btn_link)
        ),
        401,
    )


@app.errorhandler(Exception)
def general_error(e):
    return (
        render_template_string(
            error_template("Error", "예기치 못한 에러가 발생했습니다.", "홈으로", "/")
        ),
        500,
    )


@app.route("/")
def home():
    return render_template("pages/home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        username: str = form.username.data
        password: str = form.password.data

        user: User = User.query.filter(
            User.username == username, User.password == authenticator.hash(password)
        ).first()

        if user is None:
            return render_template(
                "forms/login.html", form=form, error="User not found."
            )

        response: Response = make_response(redirect(f"/s/{user.school_name}"))
        response.set_cookie("token", authenticator.generate(user))
        return response

    return render_template("forms/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form: RegisterForm = RegisterForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        username: str = form.username.data
        password: str = form.password.data
        password_confirm: str = form.password_confirm.data
        school_name: str = form.school.data

        if password != password_confirm:
            return render_template(
                "forms/register.html", form=form, error="비밀번호를 다시 입력해주세요."
            )

        if User.query.filter(User.username == username).first() is not None:
            return render_template(
                "forms/register.html", form=form, error="중복되는 아이디입니다."
            )

        school: School = School.query.filter(School.name == school_name).first()

        if school is None:
            school = School.generate(db_session, school_name)

        db_session.add(
            User(
                username=username, password=authenticator.hash(password), school=school
            )
        ), db_session.commit()

        return redirect("/login")

    return render_template("forms/register.html", form=form)


@app.route("/s/<school_name>", methods=["GET", "POST"])
@authenticator.authorize(is_abort=True)
def school_main(user: User, school: School, school_name: str):
    boards: list[Board] = Board.get(school_name)
    form: LoginForm = LoginForm(request.form)

    mfa_passed: bool = False
    error: str = ""

    if len(boards) == 0:
        abort(404)

    if request.method == "POST" and form.validate_on_submit():
        username: str = form.username.data
        password: str = form.password.data

        if user.username != username:
            error = "현재 로그인 되어 있는 사용자의 이름을 입력해주세요."
        else:
            requested_user: User = User.query.filter(
                User.username == username, User.password == authenticator.hash(password)
            ).first()

            mfa_passed = requested_user is not None

            if not mfa_passed:
                error = "인증에 실패했습니다."
            elif requested_user.school_name != school_name:
                mfa_passed = False
                error = f"{school_name}을(를) 열람할 권한이 없습니다."

    return render_template(
        "pages/school.html",
        form=form,
        school_name=school_name,
        boards=[
            board.render(visible=not (board.member_only and school.name != school_name))
            for board in Board.get(school_name)
        ],
        mfa_passed=mfa_passed,
        error=error,
    )


@app.route("/s/<school_name>/<board_id>", methods=["GET"])
@authenticator.authorize(is_abort=True)
@Board.authorize(strict=False)
def school_board(
    user: User, school: School, board: Board, school_name: str, board_id: str
):
    return render_template(
        "pages/board.html",
        school_name=school_name,
        board=board.render(
            visible=not (board.member_only and (school_name != school.name))
        ),
    )


@app.route("/s/<school_name>/<board_id>/post", methods=["GET", "POST"])
@authenticator.authorize(is_abort=True)
@Board.authorize(strict=True)
def school_post(
    user: User, school: School, board: Board, school_name: str, board_id: str
):
    form: PostForm = PostForm(request.form)

    if request.method == "POST" and form.validate_on_submit():
        title: str = form.title.data
        content: str = form.content.data

        post: Post = Post(user, school, title, content, board)
        db_session.add(post), db_session.commit()

        return redirect(f"/s/{school_name}/{board_id}/{post.id}")

    return render_template("forms/post.html", school_name=school_name, form=form)


@app.route("/s/<school_name>/<board_id>/<post_id>", methods=["GET"])
@authenticator.authorize(is_abort=True)
@Board.authorize(strict=False)
def school_post_viewer(
    user: User,
    school: School,
    board: Board,
    school_name: str,
    board_id: str,
    post_id: str,
):
    post: Post = Post.query.filter(
        Post.id == post_id, Post.school_name == school_name, Post.board_id == board_id
    ).first()

    return render_template(
        "pages/post.html",
        school_name=school_name,
        post=post,
        board=board.render(
            visible=not (board.member_only and school.name != school_name)
        ),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", 5000)))
