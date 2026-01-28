from flask import Flask,render_template, render_template_string

app = Flask(__name__)
blacklist =[]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:s>')
def E404(s):
    page = f'''
    <h1>404 : {s} Not Found</h1>
    <p>The requested URL was not found on this server.</p>
    '''
    return render_template_string(page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
