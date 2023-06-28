from django.urls import path

from . import views

from django.contrib.auth.views import (
LogoutView, 
PasswordResetView, 
PasswordResetDoneView, 
PasswordResetConfirmView,
PasswordResetCompleteView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("sign-in/",views.sign_in.as_view(),name= "sign-in"),
    path("logout/",views.logout_user,name= "logout"),
    path("create-account/",views.create_account.as_view(),name= "create-account"),
    path("email-verifictaion/",views.email_verification.as_view(),name= "email-verification"),
    # path("reset-provide-email/",views.reset_provide_email.as_view(),name = "reset-provide-email"),
    # path("reset-password/<str:uid>/<str:token>/",views.reset_password.as_view(),name ="reset-password"),


 
    path('password-reset/', PasswordResetView.as_view(template_name='authentication/reset_provide_email.html',html_email_template_name = "authentication/email_reset_text.html"),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authentication/reset_provide_email_message.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/reset_password.html'), name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='authentication/password_reset_success.html'),name='password_reset_complete'),
]