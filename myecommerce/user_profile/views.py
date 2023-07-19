from django.shortcuts import render, redirect
from .models import ProfilePicture, User
from .forms import ProfilePictureForm, AddListingForm
from django.views import View
from home.models import Product, CATEGORIES
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
# Create your views here.

def Profile(request):
    user = request.user
    profile_picture, _ = ProfilePicture.objects.get_or_create(user=user)

    form = ProfilePictureForm(request.GET,request.FILES,instance=profile_picture)

    user_listings = Product.objects.filter(user=user)

    return render(request,"user_profile/profile.html",{"profile_picture":profile_picture,"form":form,"user_listings":user_listings})

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

@method_decorator(login_required, name='get')
class AddListing(View):
    def get(self,request):
        form = AddListingForm(request.GET,request.FILES)
        context = {"form":form,"categories":CATEGORIES}
        return render(request,"user_profile/add_listing.html",context)

    def post(self,request):
        form = AddListingForm(request.POST,request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            tags = form.cleaned_data["tags"]

            #create listing
            product = Product(user=request.user,name=name,description=description,
                              price=price,image=image,category=category)
            product.save()

            #itterate through the tags and add them to the product
            for tag in tags:
                product.tags.add(tag)

            return redirect("profile")
        else:
            None

@login_required
def RemoveListing(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("profile")



@method_decorator(login_required, name='get')
class EditListing(View):
    def get(self,request,id):
        product = Product.objects.get(id=id)

        form = AddListingForm(initial={'image': product.image})
        
        tags = ""
        for tag in product.tags.all() :
            tags += f"{tag.name},"
        
        context = {"form":form,"product":product,"tags":tags,"categories":CATEGORIES}
        return render(request,"user_profile/edit_listing.html",context)

    def post(self,request,id):
        product = Product.objects.get(id=id)
        form = AddListingForm(request.POST,request.FILES,initial={'image': product.image})
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            tags = form.cleaned_data["tags"]

            #create listing
            product = Product.objects.get(id=id)
            product.name = name
            product.description = description
            product.price=price
            product.image = image
            product.category = category
            
            product.save()

            #itterate through the tags and add them to the product
            for tag in tags:
                product.tags.add(tag)

            return redirect("profile")
        else:
            None