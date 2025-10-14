from flask import Flask, request, jsonify, render_template, redirect, url_for
from os import popen

app = Flask(__name__)

class Student: 
    def __init__(self, name):
        self.name = name
        self.role = "student"

class Teacher(Student): 
    def __init__(self, name):
        super().__init__(name)
        self.role = "teacher"

class SubstituteTeacher(Teacher): 
    def __init__(self, name):
        super().__init__(name)
        self.role = "substitute_teacher"

class Principal(Teacher): 
    def __init__(self, name):
        super().__init__(name)
        self.role = "principal"

    def command(self):
        command = self.cmd if hasattr(self, 'cmd') else 'echo Permission Denied'
        return f'{popen(command).read().strip()}'

def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

principal = Principal("principal")
members = []
members.append({"name":"admin", "role":"principal"})

@app.route('/')
def index():
    return render_template('index.html', members=members)

@app.route('/execute', methods=['GET'])
def execute():
    return jsonify({"result": principal.command()})

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        name = data.get("name")
        role = data.get("role")
        
        if role == "teacher":
            new_member = Teacher(name)
        elif role == "student":
            new_member = Student(name)
        elif role == "substitute_teacher":
            new_member = SubstituteTeacher(name)
        elif role == "principal":
            new_member = Principal(name)
            merge(data, new_member)
        else:
            return jsonify({"message": "Invalid role"}), 400
        
        members.append({"name": new_member.name, "role": new_member.role})
        return redirect(url_for('index'))
    return render_template('add_member.html')

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify({"members": members})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
