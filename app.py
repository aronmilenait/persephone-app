from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    task_title = request.form['task']  
    new_task = {'id': len(tasks) + 1, 'task': task_title, 'done': False}
    tasks.append(new_task)
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
    updated_task = request.form['task']
    for task in tasks:
        if task['id'] == task_id:
            task['task'] = updated_task
            break
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
