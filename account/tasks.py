from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_mail(email, activation_code):
    massage = f"""
            Блогадарим что вы зареuестрировались на нашем сайте.
            Ваш код активации : {activation_code}
            """
    send_mail('Активация акаунта',
              massage,
              'test@gmail.com',
              [email],
              )


@shared_task
def notify_user():
    send_mail('Вечерний дайджкст',
              'Привет',
              'test@gmail.com',
              ['elabdukadyrov@gmail.com']
              )
