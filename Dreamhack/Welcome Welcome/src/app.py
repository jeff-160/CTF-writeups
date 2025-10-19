from flask import Flask, request
import os


class Context(object):
    def __init__(self, name, templates):
        self.name = name
        self.templates = templates
        self.counter = 0

    def gen_template(self):
        message = self.templates[min(self.counter, len(self.templates)-1)]
        self.counter += 1

        return message

    def render(self, fmt):
        return fmt.format(self=self)

    def __str__(self):
        return self.name


TEMPLATES_DEFAULT = [
    "Hello, {self}! Welcome to my website :D",
    "{self}, you're back!",
    "I heard that {self} once climbed Mountain Everest!",
    "{self} started to be very suspicious...",
    "Wow, {self}! You're still here?",
    "I think {self} is a very nice person.",
    "Did you know that {self} has a pet cat?",
    "I wonder what {self} is doing right now...",
]

contexts = {
    os.urandom(64).hex(): Context("Admin", ["Welcome, Admin.", "Congratulations! Here is your flag: <b>XXXXXXXXXXXXXXXXXXX</b>"]),
    "Stranger": Context("Stranger", ["Please type your name to get message!"]),
}


app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name")

    if not name:
        name = "Stranger"

    if name in contexts.keys():
        context = contexts[name]
    else:
        context = Context(name, TEMPLATES_DEFAULT)
        contexts[name] = context

    return context.render(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome message</title>
    </head>
    <body>
        <h1>Hello, {name}!</h1>

        <div>
            {context.gen_template()}
        </div>

        <h4>Please type your name!</h4>
        <form action="/" method="get">
            <input type="text" name="name" required>
            <input type="submit" value="Try it!">
        </form>
    </body>
    </html>
    """)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
