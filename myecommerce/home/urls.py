from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name= "home"),
    path("navbar/",views.navbar,name= "navbar"),
    path("cart/",views.CartView.as_view(),name = "cart")
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)