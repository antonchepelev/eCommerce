from django.shortcuts import render, redirect
from home.models import Product, CATEGORIES
from django.views import View
# Create your views here.

class SpecificCategoryView(View):
    def get(self,request,category):
        products = Product.objects.filter(category = category)
        context = {"products":products,"category":category.capitalize()}
        return render(request,"products/specific_category.html",context)
    