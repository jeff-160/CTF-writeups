import os
import re

from flask_wtf import FlaskForm
from wtforms import (
    TextField,
    TextAreaField,
    PasswordField,
    Form,
    Field,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length

if os.getenv("env", "production") == "development":
    from config import Development as AppConfig
else:
    from config import Production as AppConfig


def username_validator(form: Form, field: Field):
    if not re.search(r"^[a-z]*$", field.data):
        raise ValidationError("아이디는 영어 소문자만 가능합니다.")
    if not (4 <= len(field.data) <= 20):
        raise ValidationError("아이디는 4글자 이상, 20글자 이하이어야 합니다.")


def password_validator(form: Form, field: Field):
    if not (4 <= len(field.data) <= 20):
        raise ValidationError("비밀번호는 4글자 이상, 20글자 이하이어야 합니다.")


def school_validator(form: Form, field: Field):
    if not re.search(r"^[가-힣A-Za-z{}]*$", field.data):
        raise ValidationError("학교 이름으로 허용되지 않은 문자가 포함되어 있습니다.")
    if not (4 <= len(field.data) <= 20):
        raise ValidationError("학교 이름은 4글자 이상, 20글자 이하이어야 합니다.")
    if field.data == AppConfig.FLAG_SCHOOL:
        raise ValidationError(f"{AppConfig.FLAG_SCHOOL}는 가입할 수 없는 학교입니다.")


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False
    username = TextField("Username", validators=[DataRequired(), username_validator])
    password = PasswordField(
        "Password", validators=[DataRequired(), password_validator]
    )
    password_confirm = PasswordField(
        "Repeat Password",
        [DataRequired(), EqualTo("password", message="비밀번호를 동일하게 입력해주세요.")],
    )
    school = TextField("School", validators=[DataRequired(), school_validator])


class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = TextField("Username", validators=[DataRequired(), username_validator])
    password = PasswordField(
        "Password", validators=[DataRequired(), password_validator]
    )


class PostForm(FlaskForm):
    title = TextField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
