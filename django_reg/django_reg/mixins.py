from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class UserLoginRequiredMixin(LoginRequiredMixin):
    auth_message = 'Вы не вошли, пожалуйста, авторизуйтесь'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


# class UserIsNotAuthenticated(UserPassesTestMixin):
#     def get_test_func(self):
#         if self.request.user.is_authenticated:
#             messages.info(self.request, 'Вы уже авторизованы.')
#         return self.test_func

#     def handle_no_permission(self):
#         return redirect('home')


class UserPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request,
                       'Вы не можете изменять чужой аккаунт')
        return redirect(reverse_lazy('users'))