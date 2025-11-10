from __future__ import annotations
from typing import Dict
from uuid import uuid4
import hashlib
import time


class Password:
    data: str

    def __init__(self, data: str) -> None:
        self.data = hashlib.sha256(data.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.data == hashlib.sha256(password.encode()).hexdigest()


class Title:
    data: str
    edit_time: float

    def __init__(self, data: str) -> None:
        self.data = data
        self.edit_time = time.time()

    def get_raw_data(self):
        return self.data.strip()

    def get_title(self):
        return "Title: {0:<10}".format(self.data.strip())

    def get_title_with_edit_time(self):
        return "Title: {0:<10} (edited: {1})".format(
            self.data.strip(),
            time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.edit_time)),
        )


class Content:
    data: str
    edit_time: float

    def __init__(self, data: str) -> None:
        self.data = data
        self.edit_time = time.time()

    def get_raw_data(self):
        return self.data.strip()

    def get_content(self):
        return "Content: {0:<10}".format(self.data.strip())

    def get_content_with_edit_time(self):
        return "Content: {0:<10} (edited: {1})".format(
            self.data.strip(),
            time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.edit_time)),
        )


class Memo:
    collections: Dict[str, Memo] = {}

    title: Title
    content: Content
    password: Password

    def __init__(self, title: str, content: str, password: str):
        self.id = str(uuid4())
        self.title = Title(title)
        self.content = Content(content)
        self.password = Password(password)

    def get_raw_title(self):
        return self.title

    def get_raw_content(self):
        return self.content

    def get_title(self):
        return self.title.get_title()

    def get_content(self):
        return self.content.get_content()

    def get_title_with_edit_time(self):
        return self.title.get_title_with_edit_time()

    def get_content_with_edit_time(self):
        return self.content.get_content_with_edit_time()

    def check_password(self, password):
        return self.password.check_password(password)

    @staticmethod
    def get_memo_by_id(memo_id: str) -> Memo | None:
        return Memo.collections[memo_id] if memo_id in Memo.collections.keys() else None

    @staticmethod
    def add_memo_to_collection(memo: Memo):
        Memo.collections[memo.id] = memo
