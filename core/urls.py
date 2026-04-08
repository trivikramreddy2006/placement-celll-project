from django.contrib import admin
from django.urls import path, include
from placement.views import dashboard_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("placement/", include("placement.urls")),
    path("", dashboard_redirect, name="dashboard"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
