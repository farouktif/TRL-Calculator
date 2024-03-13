from datetime import datetime, timezone
from flask import jsonify, render_template, flash, redirect, url_for, request, abort, current_app
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
        project = Project(title=form.title.data,
                          grant_title = form.grant_title.data,
                          lead_pi = form.lead_pi.data,
                          starting_trl = form.starting_trl.data,
                          anticipated_ending_trl = form.anticipated_ending_trl.data,                           
                          description=form.description.data,
                          author=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Your project has been saved')
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

@bp.route('/api/data')
def data():
    print("*** reading project from database")
    query = Project.query    
    
    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Project.title.like(f'%{search}%'),
            Project.lead_pi.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            lead_pi = s[1:]
            if lead_pi not in ['lead_pi']:
                lead_pi = 'lead_pi'
            col = getattr(Project, lead_pi)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    return {
        'data': [project.to_dict() for project in query],
        'total': total,
    }


@bp.route('/api/data', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    project = Project.query.get(data['id'])
    for field in ['title', 'lead_pi', 'description']:
        if field in data:
            setattr(project, field, data[field])
    db.session.commit()
    return '', 204

@bp.route('/trl-questionnaire/<int:id>')
@login_required
def trl_questionnaire(id):
    project = db.first_or_404(sa.select(Project).where(Project.id == id))

    return render_template('trl_questionnaire.html', project=project)
