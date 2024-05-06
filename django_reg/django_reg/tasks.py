from celery import shared_task
from users.email import send_activate_email_message


@shared_task
def send_activate_email_message_task(user_id):
    return send_activate_email_message(user_id)
