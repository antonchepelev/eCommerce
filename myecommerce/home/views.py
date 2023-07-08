from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, CartItem
from .forms import ItemQuantityForm
from django.shortcuts import get_object_or_404
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request,"home/home.html",{"products":products})

def navbar(request):

    return render(request,"home/navbar.html")


class CartView(View):
    def dispatch(self, request, *args, **kwargs):
        self.user_cart = get_object_or_404(Cart, user__username=request.user.username)
        self.items = self.user_cart.items.all()
        self.forms = []
        for item in self.items:
            form = ItemQuantityForm(request.GET,prefix=f'form_{item}')
            self.forms.append((form,item))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        forms = []
        for item in self.items:
            form = ItemQuantityForm(request.GET,prefix=f'form_{item}')
            forms.append((form,item))
        return render(request,"home/cart.html",{"forms":forms,"items":self.items})
    
    def post(self,request):
        
        for form,item in self.forms:
        
            form = ItemQuantityForm(request.POST)
            # form.prefix = f"quantity_{item.id}"
         
            
            if form.is_valid():
                quantity = form.cleaned_data[f"quantity"]

                item_for_cart = get_object_or_404(CartItem,cart =self.user_cart, item = item)
                
                item_for_cart.quantity = quantity
                
                item_for_cart.save()

            
            
        return redirect("cart")
        
        