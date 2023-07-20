from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, CartItem, CATEGORIES
from .forms import ItemQuantityForm
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import random



# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {"products":products,"categories":CATEGORIES}
    return render(request,"home/home.html",context)

def navbar(request):

    return render(request,"home/navbar.html")



@method_decorator(login_required, name='dispatch')
class CartView(View):
    
    def dispatch(self, request, *args, **kwargs):
        
        self.cart = get_object_or_404(Cart, user__username=request.user.username)
        self.items = self.cart.items.all()
        self.cart_items = []
        self.zipped_items = zip(self.items,self.cart_items)
        for item in self.items:
            cart_item = CartItem.objects.get(cart=self.cart,item =item)
   
            self.cart_items.append(cart_item)

        
       
        

        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        #total cart cost calculation
        cart_cost_total = 0
        user_cart = CartItem.objects.filter(cart = self.cart) 
        price_tuple = zip (self.items,user_cart) #used to get the corresponding product price and quantity
        for item, cart_item in price_tuple:
            price = item.price
            quantity = cart_item.quantity
            cart_cost_total += quantity*price
        
      # Similar products to cart
        all_cart_tags = []
        cart_products = []
        for cart_item in self.cart_items:
            product = cart_item.item
            cart_products.append(product)
            product_tags = product.tags.all()
            all_cart_tags.extend(tag.name for tag in product_tags)
                
        similar_products = Product.objects.filter(tags__name__in=all_cart_tags).exclude(name__in=[product.name for product in cart_products]).distinct()
        try:
            similar_products =  random.sample(list(similar_products),4)

        except ValueError:

            similar_products = random.sample(list(similar_products),len(similar_products))
     
        return render(request,"home/cart.html",{"zipped_items":self.zipped_items,"cart_cost_total":cart_cost_total,"similar_products":similar_products})
    

        
@login_required
def ChangeItemQuantity(request, id):
    if "increase" in request.POST: 
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item=product)
        quantity = cart_item.quantity
        if request.method == "POST":
            quantity += 1
            cart_item.quantity = quantity  # Update the quantity field
            cart_item.save()
            return redirect("cart")
    
    if "decrease" in request.POST: 
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item=product)
        quantity = cart_item.quantity
        if request.method == "POST":
            if not quantity <= 1 :
                quantity = quantity - 1
                cart_item.quantity = quantity  # Update the quantity field
                cart_item.save()
            else:
                cart_item.delete()
            return redirect("cart")

@login_required
def AddCart(request, id):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    item = get_object_or_404(Product, id=id)

    # Add the item to the cart if it doesn't already exist
    if item not in cart.items.all():
        cart.items.add(item)

    # Save the cart
    cart.save()
    current_page = request.META.get('HTTP_REFERER', '/')
    return redirect(current_page)

def ProductView(request,id):
    product = Product.objects.get(id=id)
    product_tags = product.tags.all()
    tag_list = []
    for product_tag in product_tags:
        tag_list.append(product_tag.name)
    similar_products = Product.objects.filter(tags__name__in=tag_list).exclude(id=id) #match tags with other similar items
    context = {"product":product,"similar_products":similar_products.distinct()}

    return render(request,"home/product.html",context)


