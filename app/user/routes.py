from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.user.forms import EditProfileForm, EmptyForm, MessageForm
from app.models import User, Project, Message, Notification
from app.user import bp



@bp.route('/<username>')
@login_required
def user(username):    
    user = db.first_or_404(sa.select(User).where(User.username == username))
    page = request.args.get('page', 1, type=int)
    query = user.projects.select().order_by(Project.timestamp.desc())
    projects = db.paginate(query, page=page,
                        per_page=current_app.config['PROJECTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('user.user', username=user.username, page=projects.next_num) \
        if projects.has_next else None
    prev_url = url_for('user.user', username=user.username, page=projects.prev_num) \
        if projects.has_prev else None
    form = EmptyForm()
    return render_template('user/user.html', user=user, projects=projects.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/<username>/popup')
@login_required
def user_popup(username):        
    user = db.first_or_404(sa.select(User).where(User.username == username))         
    form = EmptyForm()
    return render_template('user/user_popup.html', user=user, form=form)


@bp.route('user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You no longer follow {username}.')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('main.index'))
    

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = db.first_or_404(sa.select(User).where(User.username == recipient))
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count',
                              user.unread_message_count())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user.user', username=recipient))
    return render_template('user/send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.now(timezone.utc)
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    query = current_user.messages_received.select().order_by(
        Message.timestamp.desc())
    messages = db.paginate(query, page=page,
                           per_page=current_app.config['PROJECTS_PER_PAGE'],
                           error_out=False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('user/messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    query = current_user.notifications.select().where(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    notifications = db.session.scalars(query)
    return [{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications]


@bp.route('/export_projects')
@login_required
def export_projects():
    if current_user.get_task_in_progress('export_projects'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_projects', 'Exporting projects...')
        db.session.commit()
    return redirect(url_for('user.user', username=current_user.username))