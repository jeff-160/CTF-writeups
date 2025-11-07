import time
import random
from flask import Flask, request, render_template
from jinja2 import Template
import re
import concurrent.futures

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calculate(data):
    a = data.get('a')
    b = data.get('b')

    try:
        random_sleep = random.uniform(0.1, 0.3)
        time.sleep(random_sleep)

        template_str = """
        {{ """ + a + """ + """ + b + """ }}
        """
    
        template = Template(template_str)
        result = template.render()

        return {'result': result}
    
    except Exception as e:
        return {'result': 'Error'}

def execute_with_timeout(data, timeout=0.5):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(calculate, data)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            return {'result': 'Error: Timeout'}

@app.route('/cal', methods=['POST'])
def cal():
    a = request.form.get('a')
    b = request.form.get('b')

    try:
        data = {'a': a, 'b': b}
        response = execute_with_timeout(data)
        result = response.get('result')

        pattern = r'[0-1]'
        
        if re.fullmatch(pattern, result.strip()):
            return render_template('result.html', result=result)
        else:
            return render_template('result.html', result="Only 0, 1")
    except Exception as e:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
