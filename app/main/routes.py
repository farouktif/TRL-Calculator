from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main.forms import ProjectForm
from app.models import Project
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()    


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Your project is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    projects = db.paginate(current_user.following_projects(), page=page,
                        per_page=current_app.config['PROJECTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=projects.next_num) \
        if projects.has_next else None
    prev_url = url_for('main.index', page=projects.prev_num) \
        if projects.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           projects=projects.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Project).order_by(Project.timestamp.desc())
    projects = db.paginate(query, page=page,
                        per_page=current_app.config['PROJECTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.explore', page=projects.next_num) \
        if projects.has_next else None
    prev_url = url_for('main.explore', page=projects.prev_num) \
        if projects.has_prev else None
    return render_template('index.html', title='Explore', projects=projects.items,
                           next_url=next_url, prev_url=prev_url)
