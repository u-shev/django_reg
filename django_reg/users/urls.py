from django.urls import path, include
from .views import UserCreateView, UserConfirmEmailView, \
UserListView, UserProfileView, UserUpdateView, ChangeEmailView
    # MyPasswordResetConfirmView, MyPasswordResetView

from django.views.generic import TemplateView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('<uuid:pk>/', UserProfileView.as_view(), name='profile'),
    path('<uuid:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('list', UserListView.as_view(), name='users'),
    # path('email-confirmation-sent/', TemplateView.as_view(
    #     template_name='registration/email_confirmation_sent.html'),
    #     name='email_confirmation_sent'),
    # path('email-confirmed/', TemplateView.as_view(
    #     template_name='registration/email_confirmed.html'),
    #     name='email_confirmed'),
    # path('confirm-email-failed/', TemplateView.as_view(
    #     template_name='registration/email_confirmation_failed.html'),
    #     name='email_confirmation_failed'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         UserConfirmEmailView.as_view(), name='confirm_email'),
    path("<uuid:pk>/change-email/", ChangeEmailView.as_view(), name="change_email"),
    # path("password-reset/", MyPasswordResetView.as_view(), name="password_reset"),
    # path("password-reset/done/", TemplateView.as_view(
    #     template_name='registration/password_reset_done.html'),
    #     name="password_reset_done"),
    # path("reset/<uidb64>/<token>/", MyPasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path("reset/done/", TemplateView.as_view(
    #     template_name='registration/password_reset_complete.html'),
    #     name="password_reset_complete",)
]
