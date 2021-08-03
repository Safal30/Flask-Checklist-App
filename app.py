from flask import Flask, app, render_template, request, redirect,
from flask_sqlalchemy import SQLAlchemy

#to create a requirements.txt = pip3 freeze > requirements.txt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#creating a database
db = SQLAlchemy(app)


#classes for the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #Todo title
    complete = db.Column(db.Boolean) 

#/ for index page
@app.route('/')
def index():
    #show all todos
    todo_list = Todo.query.all()

    return render_template("base.html", todo_list=todo_list)


"""Adding a NEW ITEM To the DATABASE"""
@app.route("/add", methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)

    db.session.commit()
    #redirecting to homepage
    return redirect(url_for("index"))


"""Updating an ITEM from the DATABASE"""
@app.route("/update/<int:todo_id>")
def update(todo_id):
    #query the database
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete

    db.session.commit()
    return redirect(url_for("index"))


"""Deleting an ITEM from the DATABASE"""
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #query the database to get the item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)

    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)