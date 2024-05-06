from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_reg.mixins import UserLoginRequiredMixin, UserPermissionMixin
from django_reg.tasks import send_activate_email_message_task, send_reset_pass_email_message_task
from .forms import UserForm, UserUpdateForm, EmailChangeForm
from .models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, View, ListView, \
    UpdateView, DetailView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import PasswordResetForm


class UserCreateView(SuccessMessageMixin, CreateView):

    form_class = UserForm
    template_name = 'registration/registration.html'
    extra_context = {
        'title': 'Регистрация',
        'button_text': 'Зарегистрироваться',
    }

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activate_email_message_task.delay(user.id)
        return redirect('email_confirmation_sent')


class UserUpdateView(UserLoginRequiredMixin, SuccessMessageMixin,
                     UserPermissionMixin, UpdateView):

    template_name = 'form.html'
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users')
    success_message = "Профиль успешно изменен"
    permission_message = "Вы не можете изменять чужой профиль"
    permission_url = reverse_lazy('users')
    extra_context = {
        'title': "Изменить профиль",
        'button_text': "Сохранить",
    }


class LogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('home')
    success_message = 'Вы вышли'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы вышли')
        return super().dispatch(request, *args, **kwargs)


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            user = User.objects.get(pk=uidb64)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(
          user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class UserListView(ListView):

    template_name = 'users.html'
    model = User
    context_object_name = 'users'
    queryset = User.objects.all().only('username', 'first_name', 'last_name', 'date_joined')


class UserProfileView(UserLoginRequiredMixin,
                     SuccessMessageMixin, DetailView):
    model = User
    queryset = User.objects.all().only('username', 'first_name', 'last_name', 'date_joined')
    template_name = "profile.html"
    context_object_name = "user"
    extra_context = {'title': 'Профиль',
                     'btn_update': 'Обновить'
                     }

class ChangeEmailView(UserLoginRequiredMixin, SuccessMessageMixin,
                     UserPermissionMixin, UpdateView):

    form_class = EmailChangeForm
    model = User
    template_name = 'form.html'
    success_url = reverse_lazy('users')
    success_message = "Адрес почты успешно изменен"
    permission_message = "Вы не можете изменять чужой профиль"
    permission_url = reverse_lazy('users')
    extra_context = {
        'title': 'Изменение почты',
        'button_text': 'Изменить',
    }

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.is_active = False
    #     user.save()
    #     send_activate_email_message_task.delay(user.id)
    #     return redirect('email_confirmation_sent')
    
# class MyPasswordResetView(FormView):
#     form_class = PasswordResetForm
#     template_name = 'registration/password_reset_form.html'
#     success_url = reverse_lazy("password_reset_done")
#     extra_context = {
#         'title': 'Смена пароля',
#         'button_text': 'Сменить',
#     }

#     def form_valid(self, form):
#         form.save()
#         user = self.request.user
#         send_reset_pass_email_message_task.delay(user.id)
#         return super().form_valid(form)


# class MyPasswordResetConfirmView(View):
#     def get(self, request, uidb64, token):
#         try:
#             user = User.objects.get(pk=uidb64)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(
#           user, token):
#             self.validlink = True
#             return redirect('email_confirmed')
#         else:
#             self.validlink = False
#             return redirect('email_confirmation_failed')
