import json
import sys
import time
import sqlalchemy as sa
from flask import render_template
from rq import get_current_job
from app import create_app, db
from app.models import User, Project, Task
from app.email import send_email

app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = db.session.get(Task, job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_projects(user_id):
    try:
        user = db.session.get(User, user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_projects = db.session.scalar(sa.select(sa.func.count()).select_from(
            user.projects.select().subquery()))
        for project in db.session.scalars(user.projects.select().order_by(
                Project.timestamp.asc())):
            data.append({'title': project.title,
                         'timestamp': project.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_projects)

        send_email(
            '[TRL-Calculator] Your TRL projects',
            sender=app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/export_images.txt', user=user),
            html_body=render_template('email/export_images.html', user=user),
            attachments=[('projects.json', 'application/json',
                          json.dumps({'projects': data}, indent=4))],
            sync=True)
    except Exception:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)