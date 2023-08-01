from django.urls import path

from . import views



urlpatterns = [

    path("<str:category>/",views.SpecificCategoryView.as_view(),name="specific-category"),
]