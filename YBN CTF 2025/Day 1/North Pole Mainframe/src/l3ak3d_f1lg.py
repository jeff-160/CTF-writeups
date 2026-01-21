import os
from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

app.config['l3v3l1_f1ag'] = 'REDACTED'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/level1")
def level1():
    content = render_template_string(request.args.get("name", ""))
    return render_template("level1.html", name=content)


@app.route("/level2", methods=["GET", "POST"])
def level2():
    result = ""
    if request.method == "POST":
        name = request.form.get("name", "")
        if name:
            template = f'''<p class="text-xl text-white mt-4 p-4 bg-gray-900 rounded-lg shadow-inner">
                Our records show that {name} is on the nice list!
            </p>'''
            result = render_template_string(template)

    return render_template("level2.html", result=result)


def main():
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=True)

 
if __name__ == "__main__":
    main()

