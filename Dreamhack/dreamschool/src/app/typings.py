class UserNotFoundError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NotSchoolMemberError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
