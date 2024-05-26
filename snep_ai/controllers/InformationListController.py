from flask import current_app, Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from snep_ai.database import session

import os
import snep_ai.services.InformationListService as svc_informationList
import snep_ai.services.InformationCategoryService as svc_informationCategory

informationLists = Blueprint('informationLists', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@informationLists.route('/', methods=['GET'])
@login_required
def index():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    count_informationLists, _ = svc_informationList.count()
    informationLists, error = svc_informationList.get_all()

    if error:
        flash(error, "error")

    return render_template('informationLists/index.html', active_menu='informationList', informationLists=informationLists, countinformationLists=count_informationLists[0])

@informationLists.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    error = ''

    # If the method is POST
    if request.method == 'POST':
        # Create Information List Process

        # form data
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['type']
        time_relevancy = request.form['date']

        # Check whether title exists
        informationList, error = svc_informationList.get_by_title(title)

        if informationList is None:
            # check if the post request has the file part
            if 'image' not in request.files:
                flash('No image part', "warning")
                return redirect(request.url)

            image = request.files['image']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if image.filename == '':
                flash('No selected image', "warning")
                return redirect(request.url)

            if image and allowed_file(image.filename):
                datetime_now = datetime.now()
                now = datetime.strftime(datetime_now, '%Y-%m-%d_%H-%M-%S_%f+%Z')
                joined_filename = now + "_" + image.filename

                filename = secure_filename(joined_filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))
            
            # Create the informationList and return the error (if any)
            _, error = svc_informationList.create(title=title, content=content, information_category_id=category_id, image=filename, time_relevancy=time_relevancy)

            if not error:
                flash("Information List successfully created...", "success")
                return redirect(url_for('informationLists.index'))
        else:
            flash("Information List already exists - Please try again", "warning")
            return redirect(url_for('informationLists.create'))

        if error:
            flash(error, "error")
            return redirect(url_for('informationLists.create'))

    # Category data for select form
    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    # Go to the informationList Create Form
    return render_template('informationLists/create.html', categories=categories, countCategories=count_categories[0])

@informationLists.route('/detail/<int:id>', methods=['GET'])
@login_required
def detail(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    error = ''
    informationList, error = svc_informationList.get_by_id(list_id=id)
    
    return render_template('informationLists/detail.html', detail=informationList)

@informationLists.route('/detail_news/<int:id>', methods=['GET'])
@login_required
def detail_dashboard(id):
    error = ''
    informationList, error = svc_informationList.get_by_id(list_id=id)
    
    return render_template('informationLists/detail_dashboard.html', detail=informationList)

@informationLists.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    error = ''
    informationList, error = svc_informationList.get_by_id(list_id=id)

    if request.method == 'POST':
        # Update User Process

        # form data
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['type']
        time_relevancy = request.form['date']

        # Check whether the title is unique
        informationLists, error = svc_informationList.get_all()
        count_informationList_exists = 0

        # If informationList exists
        if informationList:
            # check if the post request has the file part
            if 'image' not in request.files:
                flash('No image part', "warning")
                return redirect(request.url)

            image = request.files['image']

            if image.filename == '':
                if not error:
                    for x in informationLists:
                        if x.title == title:
                            count_informationList_exists += 1
                    
                    if count_informationList_exists == 1:
                        # If exists, then flash warning and redirect to edit form
                        flash("Title already exists - Please try again", "warning")
                        return redirect(url_for('informationLists.edit', id=id))
                else:
                    flash(error, "error")
                    return redirect(url_for('informationLists.edit', id=id))
            
            if image.filename != '':
                if image and allowed_file(image.filename):
                    datetime_now = datetime.now()
                    now = datetime.strftime(datetime_now, '%Y-%m-%d_%H-%M-%S_%f+%Z')

                    image_filename = image.filename.split(".")
                    joined_filename = now + "_" + image_filename[0] + ".jpeg"

                    filename = secure_filename(joined_filename)
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], informationList.image))
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                    # Create the informationList and return the error (if any)
                    _, error = svc_informationList.edit(list_id=id, title=title, content=content, information_category_id=category_id, image=filename, time_relevancy=time_relevancy)
            else:
                # Create the informationList and return the error (if any)
                _, error = svc_informationList.edit(list_id=id, title=title, content=content, information_category_id=category_id, time_relevancy=time_relevancy)

            if not error:
                flash("Information List successfully updated...", "success")
                return redirect(url_for('informationLists.index'))
        else:
            flash("Information List does not exists - Please try again", "warning")
            return redirect(url_for('informationLists.edit', id=id))

        if error:
            flash(error, "error")
            return redirect(url_for('informationLists.edit', id=id))

    # Category data for select form
    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    # Go to the Edit Form
    return render_template('informationLists/edit.html', informationList=informationList, categories=categories, countCategories=count_categories[0])


@informationLists.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    informationList, error = svc_informationList.get_by_id(id)
    
    if request.method == 'POST':
        # Delete InformationCategory Process

        # If informationList exists
        if informationList:
            # Delete the InformationList and return the error (if any)
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], informationList.image))
            _, error = svc_informationList.destroy(informationList.id)

            if not error:
                flash("Information List successfully deleted...", "success")
                return redirect(url_for('informationLists.index'))
        else:
            flash("Information List does not exists - Please try again", "warning")
            return redirect(url_for('informationLists.index'))

    count_informationLists, _ = svc_informationList.count()
    informationLists, error = svc_informationList.get_all()

    if error:
        flash(error, "error")

    return render_template('informationLists/index.html', active_menu='informationList', informationLists=informationLists, countinformationLists=count_informationLists[0])