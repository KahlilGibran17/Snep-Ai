from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from snep_ai.forms import LoginForm, RegisterForm
from snep_ai.models.User import User
from snep_ai.database import session

import snep_ai.services.UserService as svc_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is authenticated
    if current_user.is_authenticated:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    form = LoginForm.Form()

    # If the method is POST
    if request.method == 'POST' and form.validate_on_submit():
        # Login Process

        # form data
        username = form.username.data
        password = form.password.data

        # Check whether user exists
        user, error = svc_user.get_by_username(username)

        if error:
            flash(error, "error")

        if user:
			# Check the hash
            if check_password_hash(user.password, password):
                login_user(user)

                flash("Login successful!", "success")
                return redirect(url_for('dashboard.index'))
            else:
                flash("Incorrect password. Please try again", "warning")
                return redirect(url_for('auth.login'))
        else:
            flash("Account not found. Please check your credentials", "warning")
            return redirect(url_for('auth.login'))

    # Redirect to the Login Form
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # If the user is authenticated
    if current_user.is_authenticated:
        # Redirect to dashboard instead of the register page
        return redirect(url_for('dashboard.index'))

    form = RegisterForm.Form()

    # If the method is POST
    if request.method == 'POST' and form.validate_on_submit():
        # Register Process

        # form data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        # Check whether user exists
        user, error = svc_user.get_by_username(username)

        if error:
            flash(error, "error")

        if user is None:
            new_user = User(username=username, password=generate_password_hash(password))
            session.add(new_user)
            session.commit()

            flash("Successfully registered!", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("User already exists!", "warning")
            return redirect(url_for('auth.register'))

    # Redirect to the Register Form
    return render_template('auth/register.html', form=form)

# Logout User
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))