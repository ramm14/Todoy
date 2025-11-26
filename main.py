import random
from flask import Flask
from dotenv import load_dotenv
import os
import requests
from flask import Flask, abort, render_template, redirect, url_for, flash, request,jsonify
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey
from form import todoForm

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRETKEY")

bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)


class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(155), nullable=False)


@app.route("/", methods=['POST', 'GET'])
def home():
    response = requests.get(url="https://zenquotes.io/api/quotes/")
    quotes = response.json()
    random_quote = random.choice(quotes)
    return render_template("todo.html", quote=random_quote)


@app.route("/prototype", methods=['POST', 'GET'])
def prototype():
    todo_items = db.session.execute(db.select(Todo)).scalars().all()
    print(todo_items)
    return render_template("prototype.html", todo_items=todo_items)


@app.route("/handle-check", methods= ["POST"])
def handle_checkbox():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        return redirect(url_for('prototype'))


@app.route("/delete/<int:todo_index>")
def delete_todo(todo_index):
    todo_to_delete = Todo.query.get(todo_index)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('prototype'))


@app.route("/edit/<int:todo_index>", methods=['POST', 'GET'])
def edit_todo(todo_index):
    edit_form = todoForm()
    todo_to_edit = Todo.query.get_or_404(todo_index)
    if edit_form.validate_on_submit():
        todo_to_edit.title = edit_form.todo_header.data
        todo_to_edit.description = edit_form.todo_description.data
        db.session.commit()
        return redirect(url_for('prototype'))
    return render_template("edit.html", form=edit_form)


@app.route("/add", methods=['POST', 'GET'])
def add_todo():
    my_form = todoForm()
    if my_form.validate_on_submit():
        new_todo = Todo(title=my_form.todo_header.data, description=my_form.todo_description.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('prototype'))
    return render_template('add.html', form=my_form)


if __name__ == "__main__":
    app.run(debug=True, port=5002)

