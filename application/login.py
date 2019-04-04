##IMPORTS

from application import app #circular import because its needed for modular code. I know its ugly. Shhh.
from flask import request, render_template, redirect, flash, session #imports for various flask functions
# from os import urandom # generating random encoding
import hashlib #library for hashing (fairly self-explanatory :P)
from .db_connect import *

###LOGIN THE USER
@app.route('/login/', methods=['POST'])
def login():
	# get form information
	form_data = request.form

	# validation
	if form_data['username'] == "":
		flash("The username field is required.")
		return redirect("/")
	if form_data['password'] == "":
		flash("The password field is required.")
		return redirect("/")

	#get data from database
	data = query_db("SELECT password, isTeacher, id FROM people WHERE username=? LIMIT 1", [form_data['username']])
	#make sure username is right
	if data == []:
		flash("Your username was incorrect.")
		return redirect("/")

	# check the password
	user_pass = form_data['password']
	if data[0][0] == user_pass:
		#correct password
		session['isTeacher'] = data[0][1]
		session['id'] = data[0][2]
		#if student, redirect to students page
		if session['isTeacher'] == 0:
			return redirect("/students/")
		#else they are a teacher, redirect to teachers page
		else:
			return redirect("/teachers/")

	flash("Your password was incorrect.")
	return redirect("/")

###REGISTER THE USER
@app.route('/register/', methods=['GET', 'POST'])
def register():

	#form data is GET, so render template
	if request.method == 'GET':
		return render_template('register.html')

	#request method is POST, so do everything

	form_data = request.form

	#form validation
	if form_data['username'] == "" or form_data['password'] == "" or form_data['name'] == "" or form_data['email'] == "":
		return "All text fields are required"
	if not 'isTeacher' in form_data:
		isTeacher = 0 # they are not a teacher
	else:
		isTeacher = 1 # they are a teacher

	password = form_data['password']
	insert_db("INSERT INTO people (isTeacher, username, password, name, email) VALUES (?, ?, ?, ?, ?)", [isTeacher, form_data['username'], password, form_data['name'], form_data['email']])
	flash("The entry was created")
	return redirect("/register/")
