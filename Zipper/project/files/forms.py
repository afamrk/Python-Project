from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired

class LinkForm(FlaskForm):
    link = URLField('Url', validators=[DataRequired()],
            render_kw={"class":"bg-light form-control border-0 small","placeholder":"Paste url"})
    submit = SubmitField('good')

class AdvancedForm(FlaskForm):
    link = URLField('Url', validators=[DataRequired()],
            render_kw={"class":"form-control", "id":"url", "placeholder":"https://example.com/file.zip"})
    level = SelectField('Select', choices=[('high', 'high'), ('medium', 'Medium'), ('low', 'low')],
            render_kw={"class":"form-select"})
    split = SelectField('Select', choices=[('None', 'N/A'), ('5', '50MB'), ('100', '100MB'), ('250', '250MB'), ('500', '500MB'), ('1000', '1GB')], render_kw={"class":"form-select"})
    format = SelectField('Select', choices=[('7zip', '7Zip'), ('rar', 'Rar'), ('zip', 'Zip')], render_kw={"class":"form-select"})
    submit = SubmitField('good')

