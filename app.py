from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import re
import logging

app = Flask(__name__)

# Configuration for the app
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session Configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['SESSION_USE_SIGNER'] = True  # Use a secure cookie with a signer

# Initialize CSRF protection and database
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# Logging setup
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Define the model
class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"

# Define the form class
class FirstForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

# Function to validate input against malicious scripts
def is_input_safe(input_string):
    # Define a regular expression for safe input (only letters and spaces)
    return re.match("^[A-Za-z ]*$", input_string) is not None

# Main route to handle GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    form = FirstForm()
    if form.validate_on_submit():  # Validate the form on submission
        fname = form.fname.data.strip()  # Remove leading/trailing whitespace
        lname = form.lname.data.strip()  # Remove leading/trailing whitespace
        email = form.email.data.strip()    # Remove leading/trailing whitespace

        # Validate input safety
        if not (is_input_safe(fname) and is_input_safe(lname)):
            print("Invalid input detected!")
            return render_template('index.html', allpeople=FirstApp.query.all(), form=form)

        # Create a new entry
        new_entry = FirstApp(fname=fname, lname=lname, email=email)

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/')  # Redirect to avoid form re-submission
        except Exception as e:
            app.logger.error(f"Error occurred: {e}")  # Log the error
            db.session.rollback()  # Rollback in case of error

    # Fetch all records from the database
    allpeople = FirstApp.query.all()
    return render_template('index.html', allpeople=allpeople, form=form)

@app.route('/delete/<int:sno>', methods=['GET'])
def delete(sno):
    record = FirstApp.query.filter_by(sno=sno).first()
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    record = FirstApp.query.filter_by(sno=sno).first()
    form = FirstForm(obj=record)  # Pre-populate the form with existing data
    if request.method == 'POST' and form.validate_on_submit():
        fname = form.fname.data.strip()
        lname = form.lname.data.strip()
        email = form.email.data.strip()

        # Validate input safety
        if not (is_input_safe(fname) and is_input_safe(lname)):
            print("Invalid input detected!")
            return render_template('update.html', form=form)

        # Update the record
        record.fname = fname
        record.lname = lname
        record.email = email
        db.session.commit()
        return redirect('/')
    return render_template('update.html', form=form)

@app.route('/home')
def home():
    return 'Welcome To The Home Page'

# Error handling for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Error handling for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Internal Server Error: {e}")  # Log the error
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
