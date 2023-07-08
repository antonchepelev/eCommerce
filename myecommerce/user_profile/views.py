from django.shortcuts import render, redirect
from .models import ProfilePicture, User
from .forms import ProfilePictureForm, AddListingForm
from django.views import View
from home.models import Product
# Create your views here.

def Profile(request):
    user = request.user
    profile_picture, _ = ProfilePicture.objects.get_or_create(user=user)

    form = ProfilePictureForm(request.GET,request.FILES,instance=profile_picture)
    return render(request,"user_profile/profile.html",{"profile_picture":profile_picture,"form":form})

def UpdateProfile(request):
    user = request.user
    profile_picture, _ = ProfilePicture.objects.get_or_create(user=user)
    
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile_picture)
        if form.is_valid():
            form.save()
            new_first_name = request.POST.get("first_name")
            new_last_name = request.POST.get("last_name")
            new_username = request.POST.get("username")

            #check if there are any changes in User model attributes, if there is , they will be updated
            user = User.objects.get(username = request.user.username)
            if not user.first_name == new_first_name:
                user.first_name = new_first_name

            if not user.last_name == new_last_name:
                user.last_name = new_last_name

            if not user.username == new_username:
                user.username = new_username
            user.save()
            return redirect("profile")
    else:
        form = ProfilePictureForm(instance=profile_picture)

    return render(request, "user_profile/profile.html", {"profile_picture": profile_picture, "form": form})


class AddListing(View):
    def get(self,request):
        form = AddListingForm(request.GET,request.FILES)
        context = {"form":form}
        return render(request,"user_profile/add_listing.html",context)

    def post(self,request):
        form = AddListingForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            tags = form.cleaned_data["tags"]

            #create listing
            product = Product(user=request.user,name=name,description=description,
                              price=price,image=image)
            product.save()

            #itterate through the tags and add them to the product
            for tag in tags:
                product.tags.add(tag)

            return redirect("profile")
        else:
            None
        