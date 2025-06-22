from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from myapp.admindossier.sites import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 