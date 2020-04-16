from django.core.mail import send_mail
from celery import shared_task

from main import constants

@shared_task
def send_mail_to_manager(mail, id):
    send_mail(
        subject='У вас новая заявка № ' + str(id),
        message = 'Чтобы посмотреть заявку перейдите по ссылке http://localhost:8000/admin/main/application/' + str(id) + "/",
        from_email = constants.GMAIL_EMAIL,
        recipient_list = [mail, ],
        fail_silently = False,
    )