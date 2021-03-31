# -*- coding: utf-8 -*-
from flask import (
    Flask,
    request,
    render_template,
    jsonify,
    url_for
)
from make_celery import make_celery
from flask_mail import Mail, Message
import random
import time

flask_app = Flask(__name__)
flask_app.config.from_object('settings')
mail = Mail(flask_app)
celery = make_celery(flask_app)


@celery.task(name="mail_demo.mail_sender")
def mail_sender(receiver, username):
    email_data = {
        "subject": "Happy to join us, {}".format(username),
        "to": receiver,
        "body": "Welcome to jon us!"
    }
    msg = Message(
        email_data["subject"],
        sender = flask_app.config["MAIL_DEFAULT_SENDER"],
        recipients = [email_data["to"]]
    )
    msg.body = email_data['body']
    with flask_app.app_context():
        mail.send(msg)


@celery.task(name="celery_demo.long_task", bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@flask_app.route("/send/mail/", methods=["GET", "POST"])
def send_email():
    params = request.get_json()
    receiver = params.get("receiver")
    username = params.get("username")
    mail_sender.delay(receiver, username)
    return "Hello, {}. Confirm mail sent already, please check your mailbox.".format(username)


@flask_app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({"task_id": task.id}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@flask_app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
  

if __name__ == "__main__":
    flask_app.run()
