from functools import wraps
import datetime
import uuid
import os
import string
import random

from flask import abort
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

if os.getenv("env", "production") == "development":
    from config import Development as AppConfig
else:
    from config import Production as AppConfig

engine = create_engine(
    AppConfig.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


class School(Base):
    __tablename__ = "school"

    pk = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)

    user = relationship("User", back_populates=__tablename__)
    post = relationship("Post", back_populates=__tablename__)
    board = relationship("Board", back_populates=__tablename__)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.__tablename__} {self.name}>"

    @staticmethod
    def generate(
        _db_session: scoped_session, school_name: str, is_commit: bool = False
    ):
        _school = School(school_name)
        db_session.add(_school)
        Board.generate(_db_session, _school)
        if is_commit:
            _db_session.commit()
        return _school


class Board(Base):
    __tablename__ = "board"

    pk = Column(Integer, primary_key=True)

    id = Column(String(200), nullable=False)
    name = Column(String(200), nullable=False)

    member_only = Column(Boolean, nullable=False)
    mfa_enabled = Column(Boolean, nullable=False)

    post = relationship("Post", back_populates=__tablename__)

    school = relationship("School", back_populates=__tablename__)
    school_name = Column(String(100), ForeignKey("school.name"))

    def __init__(
        self,
        board_id: str,
        name: str,
        school: School,
        member_only: bool,
        mfa_enabled: bool,
    ):
        self.id = board_id
        self.name = name
        self.school = school
        self.member_only = member_only
        self.mfa_enabled = mfa_enabled

    def __repr__(self):
        return f"<{self.__tablename__} ({self.school_name}) {self.name}>"

    def render(self, visible: bool):
        return {"data": self, "visible": visible}

    @staticmethod
    def generate(_db_session: scoped_session, school: School, is_commit: bool = False):
        free_board_id, secret_board_id = uuid.uuid1(), uuid.uuid1()
        db_session.add(
            Board(str(free_board_id), "자유게시판", school, member_only=False, mfa_enabled=False)
        )
        db_session.add(
            Board(str(secret_board_id), "비밀게시판", school, member_only=True, mfa_enabled=False)
        )

        if is_commit:
            db_session.commit()

    @staticmethod
    def get(school_name: str, board_id: str = None) -> list["Board"]:
        query = Board.query.filter(Board.school_name == school_name)

        if board_id:
            query = query.filter(Board.id == board_id)

        return query.all()

    @staticmethod
    def authorize(strict: bool):
        def decorator(f):
            @wraps(f)
            def wrapper(
                user: User,
                school: School,
                school_name: str,
                board_id: str,
                *args,
                **kwargs,
            ):
                boards: list["Board"] = Board.get(school_name, board_id)

                if len(boards) == 0:
                    abort(404)
                elif boards[0].member_only and school.name != school_name:
                    abort(401)
                elif strict and school.name != school_name:
                    abort(401)

                return f(
                    user, school, boards[0], school_name, board_id, *args, **kwargs
                )

            return wrapper

        return decorator


class User(Base):
    __tablename__ = "user"

    pk = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    school = relationship("School", back_populates=__tablename__)
    school_name = Column(String(100), ForeignKey("school.name"))

    post = relationship("Post", back_populates=__tablename__)

    def __init__(self, username: str, password: str, school: School):
        self.username = username
        self.password = password
        self.school = school

    def __repr__(self):
        return f"<{self.__tablename__} ({self.school_name}) {self.username}>"


class Post(Base):
    __tablename__ = "post"

    pk = Column(Integer, primary_key=True)
    id = Column(String(50), default=lambda x: str(uuid.uuid1()))
    title = Column(String(300), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates=__tablename__)
    username = Column(String(100), ForeignKey("user.username"))

    school = relationship("School", back_populates=__tablename__)
    school_name = Column(String(100), ForeignKey("school.name"))

    board = relationship("Board", back_populates=__tablename__)
    board_id = Column(String(100), ForeignKey("board.id"))

    def __init__(
        self, user: User, school: School, title: str, content: str, board: Board
    ):
        self.user = user
        self.school = school
        self.title = title
        self.content = content
        self.board = board

    def __repr__(self):
        return f"<{self.__tablename__} ({self.school_name}) {self.title}>"


def init_db():
    Base.metadata.create_all(bind=engine)


def setup_challenge():
    def random_name(n):
        return "".join([random.choice(string.ascii_letters) for _ in range(n)])

    flag_school_name = AppConfig.FLAG_SCHOOL

    if School.query.filter(School.name == flag_school_name).first() is not None:
        return

    flag_school: School = School.generate(db_session, flag_school_name, False)

    flag_user: User = User(random_name(64), random_name(64), flag_school)
    db_session.add(flag_user)

    db_session.commit()

    flag_board: Board = Board.query.filter(
        Board.school == flag_school, Board.member_only
    ).first()
    flag_post: Post = Post(
        flag_user,
        flag_school,
        "FLAG",
        os.environ.pop("FLAG", "dh{THIS IS NOT FLAG}"),
        flag_board,
    )
    db_session.add(flag_post)

    flag_board.mfa_enabled = True
    db_session.commit()


init_db()
setup_challenge()
