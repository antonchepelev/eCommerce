from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


CATEGORIES = (
    ('other', 'Other'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home', 'Home'),
        ('beauty', 'Beauty'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('jewelry', 'Jewelry'),
        ('automotive', 'Automotive'),
        ('health', 'Health'),
        ('food', 'Food'),
        ('music', 'Music'),
        ('movies', 'Movies'),
        # Add more categories as needed
    )

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    category = models.CharField(max_length=50,null = True, blank=True, choices = CATEGORIES)
    tags = TaggableManager()

    def __str__(self):
        return self.name


class Cart(models.Model):
    items = models.ManyToManyField(Product,through='CartItem')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s cart "


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE,unique=False)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart} {self.item} ({self.quantity}) "