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

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    task_title = request.form['task']

    new_task = Task(task=task_title)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
    task_title = request.form['task']

    task = Task.query.get(task_id)
    if task:
        task.task = task_title  
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
