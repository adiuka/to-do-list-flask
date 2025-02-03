from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_ckeditor import CKEditorField


# WTForm for a new task
class CreateTaskForm(FlaskForm):
    """The Form Class to Define the Task Objects that will be Displayed once made"""
    title = StringField("Task Title", validators=[DataRequired()])
    author = StringField("Asignee", validators=[DataRequired()])
    due_date = DateTimeLocalField("Due Date",
                                  format="%Y-%m-%dT%H:%M",
                                  validators=[Optional()]
                                  )
    description = CKEditorField("Description of Task", validators=[Optional()])
    priority = SelectField(
        "Priority",
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        validators=[DataRequired()],
        default="low"
    )
    submit = SubmitField("Submit")