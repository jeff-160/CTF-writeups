from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# The UI Template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_data()
    return jsonify({"status": "success", "message": "Data received."}), 200


@app.route('/admin/flag', methods=['GET', 'POST'])
def flag():
    return "EHAX{TEST_FLAG}\n", 200


@app.errorhandler(404)
def not_found(e):
    return "Not Found\n", 404
