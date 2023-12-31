from django.urls import path

from . import views


urlpatterns = [
    path("profile/",views.Profile,name = "profile"),
    path("profile/upload-profile-picture",views.UpdateProfile,name ="upload-profile-picture"),
    path("profile/add-listing",views.AddListing.as_view(),name = "add-listing"),
    path("profile/remove-listing/<int:id>/",views.RemoveListing,name = "remove-listing"),
    path("profile/edit-listing/<int:id>/",views.EditListing.as_view(),name = "edit-listing"),
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)