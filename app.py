import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

instance_path = os.path.join(app.root_path, 'instance')
db_file_path = os.path.join(instance_path, 'tasks.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

def contains_disallowed_characters(text):
    disallowed_chars = {';', '<', '>', '-', '/'}
    return any(char in disallowed_chars for char in text)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    task_title = request.form['task']
    
    if len(task_title) > 55:
        error_message = 'Task must be less than 55 characters'
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks, error_message=error_message)
    
    if contains_disallowed_characters(task_title):
        error_message = 'Task contains disallowed characters'
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks, error_message=error_message)

    new_task = Task(task=task_title)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    edited_task_title = request.form.get('task')
    
    if len(edited_task_title) > 55:
        error_message = 'Task must be less than 55 characters'
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks, error_message=error_message)
    
    if contains_disallowed_characters(edited_task_title):
        error_message = 'Task contains disallowed characters'
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks, error_message=error_message)

    task = Task.query.get(task_id)
    if task:
        task.task = edited_task_title
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)