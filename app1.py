from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# API endpoints
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        tasks_data = [{'id': task.id, 'title': task.title} for task in tasks]
        return jsonify(tasks_data)
    elif request.method == 'POST':
        data = request.json
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'PUT':
        data = request.json
        task.title = data['title']
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title}), 200
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)

