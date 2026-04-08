from django.contrib import admin
from django.urls import path, include
from placement.views import dashboard_redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("placement/", include("placement.urls")),
    path("", dashboard_redirect, name="dashboard"),
]
