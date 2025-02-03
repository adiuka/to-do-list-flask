from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime, Text
from flask_bootstrap import Bootstrap5
from datetime import datetime
from forms import CreateTaskForm


app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = "YOUR KEY HERE"
db = SQLAlchemy(model_class=Base)
Bootstrap5(app)
db.init_app(app)


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(10), default="low")
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """The approute that renders the homepage and sorts all the data by date. Soonest fiorst and null values at the very bottom"""
    tasks = Task.query.order_by(Task.due_date.asc().nulls_last()).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """The app route that allows you to create a new task"""
    form = CreateTaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            author=form.author.data,
            due_date=form.due_date.data,
            description=form.description.data,
            priority=form.priority.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("new_task.html", form=form)


@app.route("/task/<int:task_id>", methods=["GET"])
def show_task(task_id):
    """The app route that shows a task in greater detail, allowing you to see the description etc."""
    task = Task.query.get_or_404(task_id)
    return render_template('show_task.html', task=task)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """The app route that deletes a specific task"""
    task_to_delete = Task.query.get(task_id)

    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task Deleted", "success")
    
    else:
        flash("Task Not Found", "danger")

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """The app route that makes tasks complete and incomplete"""
    task = Task.query.get_or_404(task_id)

     # If the task is already completed, uncheck it (set to False)
    if task.completed:
        task.completed = False
    else:
        # Otherwise, mark it as completed (set to True)
        task.completed = True

    db.session.commit()
    return redirect(url_for('index'))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """App rout to Edit a Specific Task"""
    task = Task.query.get_or_404(task_id)
    # Creates a new Form object and takes the variables from the query
    edit_form = CreateTaskForm(
        title=task.title,
        author=task.author,
        due_date=task.due_date,
        description=task.description,
        priority=task.priority
    )
    # If it is valid, it then updates it with the new variables
    if edit_form.validate_on_submit():
        task.title = edit_form.title.data
        task.author = edit_form.author.data
        task.due_date = edit_form.due_date.data
        task.description = edit_form.description.data
        task.priority = edit_form.priority.data
        db.session.commit()
        # Will show the post in question
        return redirect(url_for("show_task", task_id=task.id))
    # Will first of all render the new_task page with all the required information
    return render_template("new_task.html", form=edit_form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
