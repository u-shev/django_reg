from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()


def send_activate_email_message(user_id):

    user = get_object_or_404(User, id=user_id)
    token = default_token_generator.make_token(user)
    uid = user.pk
    activation_url = reverse_lazy('confirm_email',
                                  kwargs={'uidb64': uid, 'token': token})
    subject = f'Активируйте свой аккаунт, {user.username}!'
    message = render_to_string('registration/email_text.html', {
        'user': user,
        'activation_url': f'http://127.0.0.1:8000{activation_url}',
    })
    return user.email_user(subject, message)
