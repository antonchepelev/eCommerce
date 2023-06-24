from django.urls import path

from . import views

urlpatterns = [
    path("sign-in/",views.sign_in.as_view(),name= "sign-in"),
    path("logout/",views.logout_user,name= "logout"),
    path("create-account/",views.create_account.as_view(),name= "create-account"),
    path("email-verifictaion/",views.email_verification.as_view(),name= "email-verification"),
]