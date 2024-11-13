from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    complete = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    sort = request.args.get('sort', '')
    filter_by = request.args.get('filter', '')

    todos = db.session.query(Todo)

    if filter_by == 'completed':
        todos = todos.filter(Todo.complete.is_(True))
    elif filter_by == 'incomplete':
        todos = todos.filter(Todo.complete.is_(False))

    if sort == 'created_at_asc':
        todos = todos.order_by(Todo.created_at.asc())  
    elif sort == 'created_at_desc':
        todos = todos.order_by(Todo.created_at.desc())  
    elif sort == 'completed_first':
        todos = todos.order_by(Todo.complete.desc(), Todo.created_at.asc())
    elif sort == 'incomplete_first':
        todos = todos.order_by(Todo.complete.asc(), Todo.created_at.asc())  

    todos = todos.all()

    return render_template("base.html", todo_list=todos)

@app.post("/add")
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    new_todo = Todo(title=title, description = description, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.post("/edit/<int:todo_id>")
def edit(todo_id):
    title = request.form.get("title")
    description = request.form.get("description")
    
    if title and description:
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        todo.title = title
        todo.description = description
        db.session.commit()

    return redirect(url_for("home"))

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))