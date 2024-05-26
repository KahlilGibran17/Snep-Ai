from flask import Blueprint, request, render_template, flash, redirect, url_for
import snep_ai.services.InformationCategoryService as svc_informationCategory
from flask_login import login_required, current_user

informationCategory = Blueprint('informationCategory', __name__)

@informationCategory.route("/categories", methods=['GET'])
@login_required
def index():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    if error:
        flash(error, "error")

    return render_template('categories/index.html', active_menu='categories', categories=categories, countCategories=count_categories[0])

@informationCategory.route('/categories/create', methods=['POST'])
@login_required
def create():
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    # If the method is POST
    if request.method == 'POST':
        # Create InformationCategory Process

        # form data
        form_label = request.form['category_label']
        label = form_label.title()

        # Check whether InformationCategory exists
        category, error = svc_informationCategory.get_by_name(label)

        if category is None:
            # Create the InformationCategory and return the error (if any)
            _, error = svc_informationCategory.create(label)

            if not error:
                flash("Category successfully created...", "success")
                return redirect(url_for('informationCategory.index'))
        else:
            flash("Category already exists - Please try again", "warning")
            return redirect(url_for('informationCategory.index'))

        if error:
            flash(error, "error")
            return redirect(url_for('informationCategory.index'))

@informationCategory.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))
    
    category, error = svc_informationCategory.get_by_id(id)

    if request.method == 'POST':
        # Update InformationCategory Process
        
        # form data
        form_label = request.form['category_label']
        label = form_label.title()
        
        # Check whether the label from InformationCategory is unique
        categories, error = svc_informationCategory.get_all()
        count_category_exists = 0

        if not error:
            for x in categories:
                if x.label == label:
                    count_category_exists += 1
            
            if count_category_exists == 1:
                # If exists, then flash warning and redirect to edit form
                flash("Category already exists - Please try again", "warning")
                return redirect(url_for('informationCategory.edit', id=id))
        else:
            flash(error, "error")
            return redirect(url_for('informationCategory.edit', id=id))
        
        # If category exists
        if category:
            # Delete the category and return the error (if any)
            _, error = svc_informationCategory.edit(id, label)

            if not error:
                flash("Category successfully updated...", "success")
                return redirect(url_for('informationCategory.index'))
        else:
            flash("Category does not exists - Please try again", "warning")
            return redirect(url_for('informationCategory.index'))

    return render_template('categories/edit.html', active_menu='categories', category=category)

@informationCategory.route('/categories/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    # If the user is not admin
    if not current_user.is_admin:
        # Redirect to dashboard instead of the login page
        return redirect(url_for('dashboard.index'))

    category, error = svc_informationCategory.get_by_id(id)
    
    if request.method == 'POST':
        # Delete InformationCategory Process

        # If category exists
        if category:
            # Delete the InformationCategory and return the error (if any)
            _, error = svc_informationCategory.destroy(category.id)

            if not error:
                flash("Category successfully deleted...", "success")
                return redirect(url_for('informationCategory.index'))
        else:
            flash("Category does not exists - Please try again", "warning")
            return redirect(url_for('informationCategory.index'))

    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    if error:
        flash(error, "error")

    return render_template('categories/index.html', active_menu='categories', categories=categories, countCategories=count_categories[0])

@informationCategory.route("/geInformationCategory", methods=['GET'])
@login_required
def get_InformationCategory():
    # fetch from db
    informationCategory, error = svc_informationCategory.getInformationCategory(id)
    if error:
        flash(error)
        isSuccess = False
    else:
        isSuccess = True

    # map list into json
    response = []
    for category in informationCategory:
        response.append({
            "id": category.id,
            "label": category.label
        })

    # return response
    return {
        "isSuccess": isSuccess,
        "chatLog": response
    }