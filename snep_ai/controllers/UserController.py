from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from snep_ai.forms import UserForm
from snep_ai.database import session

import snep_ai.services.UserService as svc_user

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
@login_required
def index():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    count_users, _ = svc_user.count()
    users, error = svc_user.get_all()

    if error:
        flash(error, "error")

    return render_template('users/index.html', active_menu='users', users=users, countUsers=count_users[0])

@users.route('/account/<int:id>', methods=['GET', 'POST'])
def account(id):
    error = ''
    user, error = svc_user.get_by_id(user_id=id)
    form = UserForm.EditForm()

    # Checked the user
    if current_user.id != user.id:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST' and form.validate_on_submit():
        # Update User Process

        # Form Data from user input
        username = form.username.data
        password = form.password.data

        # Check whether the username is unique
        users, error = svc_user.get_all()
        count_user_exists = 0

        if not error:
            for x in users:
                if x.username == username:
                    count_user_exists += 1
            
            if count_user_exists == 1:
                # If exists, then flash warning and redirect to edit form
                flash("Username already exists - Please try again", "warning")
                return redirect(url_for('users.account', id=id))
        else:
            flash(error, "error")
            return redirect(url_for('users.account', id=id))


        # If user exists
        if user:
            # If password from user input has value
            if password:
                # Hash the password
                hash_password = generate_password_hash(password)

                # Update the user and return the error (if any)
                _, error = svc_user.edit(id, username, hash_password)
            else :
                # Update the user and return the error (if any)
                _, error = svc_user.edit(id, username)

            if not error:
                flash("User successfully updated...", "success")
                return redirect(url_for('users.account', id=id))
        else:
            flash("User does not exists - Please try again", "warning")
            return redirect(url_for('users.account', id=id))

        if error:
            flash(error, "error")
            return redirect(url_for('users.account', id=id))

    # Form Data in Edit Form
    form.username.data = user.username
    
    return render_template('account/account.html', active_menu='account', form=form, user=user)

@users.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    error = ''
    form = UserForm.CreateForm()

    # If the method is POST
    if request.method == 'POST' and form.validate_on_submit():
        # Create User Process

        # form data
        username = form.username.data
        password = form.password.data
        role = form.role.data

        # Check whether user exists
        user, error = svc_user.get_by_username(username)

        if user is None:
            # Hash the password
            hash_password = generate_password_hash(password)

            if role == "true":
                # Create the user and return the error (if any)
                _, error = svc_user.create(uname=username, hash_pass=hash_password, role=True)
            else:
                # Create the user and return the error (if any)
                _, error = svc_user.create(uname=username, hash_pass=hash_password, role=False)

            if not error:
                flash("User successfully created...", "success")
                return redirect(url_for('users.index'))
        else:
            flash("User already exists - Please try again", "warning")
            return redirect(url_for('users.create'))

        if error:
            flash(error, "error")
            return redirect(url_for('users.create'))

    # Go to the User Form
    return render_template('users/create.html', form=form)

@users.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    error = ''
    user, error = svc_user.get_by_id(user_id=id)
    form = UserForm.EditForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Update User Process

        # Form Data from user input
        username = form.username.data
        password = form.password.data

        # Check whether the username is unique
        users, error = svc_user.get_all()
        count_user_exists = 0

        if not error:
            for x in users:
                if x.username == username:
                    count_user_exists += 1
            
            if count_user_exists == 1:
                # If exists, then flash warning and redirect to edit form
                flash("Username already exists - Please try again", "warning")
                return redirect(url_for('users.edit', id=id))
        else:
            flash(error, "error")
            return redirect(url_for('users.edit', id=id))


        # If user exists
        if user:
            # If password from user input has value
            if password:
                # Hash the password
                hash_password = generate_password_hash(password)

                # Update the user and return the error (if any)
                _, error = svc_user.edit(id, username, hash_password)
            else :
                # Update the user and return the error (if any)
                _, error = svc_user.edit(id, username)

            if not error:
                flash("User successfully updated...", "success")
                return redirect(url_for('users.index'))
        else:
            flash("User does not exists - Please try again", "warning")
            return redirect(url_for('users.edit', id=id))

        if error:
            flash(error, "error")
            return redirect(url_for('users.edit', id=id))

    # Form Data in Edit Form
    form.username.data = user.username
    
    # Go to the Edit User Form
    return render_template('users/edit.html', form=form, user=user)

@users.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    user, error = svc_user.get_by_id(user_id=id)

    if current_user.id == user.id:
        flash("You can not delete yourself!", "warning")
        return redirect(url_for('users.index'))

    if request.method == 'POST':
        # Delete User Process

        # If user exists
        if user:
            # Delete the user and return the error (if any)
            _, error = svc_user.destroy(user.id)

            if not error:
                flash("User successfully deleted...", "success")
                return redirect(url_for('users.index'))
        else:
            flash("User does not exists - Please try again", "warning")
            return redirect(url_for('users.index'))
        

    count_users, _ = svc_user.count()
    users, error = svc_user.get_all()

    if error:
        flash(error, "error")

    return render_template('users/index.html', active_menu='users', users=users, countUsers=count_users[0])
