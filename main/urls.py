from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from django.urls import include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("cyrap/", include("cyrap.urls")),
]

if settings.DEBUG is False:
    urlpatterns = [path("v1/api/", include(urlpatterns))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
