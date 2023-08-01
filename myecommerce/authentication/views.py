
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import CreateAccountForm, LoginForm, EmailVerificationForm
from django.contrib.auth import authenticate, login, logout
from .models import UserManager
from django.core.mail import send_mail
import random
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Create your views here.


class Login(View):
    def get(self, request):
        if request.method == 'GET':
            form = LoginForm(request.GET)
            return render(request, 'authentication/sign_in.html', {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(
                    request, username=username, password=password)
                user_verification = User.objects.get(username=username)

                # if user is_active = False they will be redirected to email verification page to confirm their email
                #the sessions are used to send out and use the info for the email/ verification
                if user_verification.is_active == False:
                    email = user_verification.email
                    first_name = user_verification.first_name
                    request.session["username"] = username
                    request.session["email"] = email
                    request.session["first_name"] = first_name
                    return redirect("email-verification")
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Invalid username or password.')
        else:
            form = LoginForm()
        return render(request, 'authentication/sign_in.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect("home")


class CreateAccount(View):
    def get(self, request):
        if request.method == "GET":
            form = CreateAccountForm(request.GET)
            return render(request, "authentication/create_account.html", {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                user = UserManager.create_user(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()

                # used for personalized emails / identification
                request.session["email"] = email
                request.session["first_name"] = first_name
                request.session["username"] = username

                return redirect("email-verification")

            else:
                form = CreateAccountForm()
                return render(request, "authentication/create_account.html", {'form': form})


class EmailVerification(View):
    def get(self, request):

        form = EmailVerificationForm(request.GET)
        # session cookie data is used to personalize the email
        email = request.session.get("email")
        first_name = request.session.get("first_name")
        email_confirmation_number = random.randint(1000000000, 9999999999)
        context = {"email_confirmation_number": email_confirmation_number,
                   "first_name": first_name}
        html_order_number = render_to_string(
            "authentication/email_text.html", context)
        send_mail(
            "Please Verify Your Email Address",
            "",
            "cloudbazaronline@gmail.com",
            [email],
            html_message=html_order_number,
            fail_silently=False,
        )

        request.session["email_confirmation_number"] = email_confirmation_number
        # if the resend code button is clicked and it goes through successfully it will display a message
        if "resend-code" in request.GET:
            resend_code = True
        else:
            resend_code = False

        # works like a delete button for the displayed message
        if "delete-resend-msg" in request.GET:
            resend_code = False

            context = {"form": form, "resend_code": resend_code}

            return render(request, "authentication/email_verification.html", context)

        context =  {"form": form, "resend_code": resend_code}
        
        return render(request, "authentication/email_verification.html",context)

    def post(self, request):

        username = request.session.get("username")
        # form submission to verify email
        if "confirmation_number" in request.POST:
            form = EmailVerificationForm(request.POST)
            if form.is_valid():
                email_confirmation_number = request.session.get(
                    "email_confirmation_number")
                confirmation_number = form.cleaned_data["confirmation_number"]

                # filter user to update the is_active to True if they confirm their email
                user = User.objects.get(username=username)

                if confirmation_number == str(email_confirmation_number):
                    # update user status to active to avoid triggering email confirmation
                    user.is_active = True

                    user.save()
                    return redirect("sign-in")
                else:
                    form.add_error("confirmation_number",
                                   "Please provide a valid confirmation number")
                    # form.add_error("confirmation_number",confirmation_number)

            else:
                form = EmailVerificationForm()
        return render(request, "authentication/email_verification.html", {"form": form})
