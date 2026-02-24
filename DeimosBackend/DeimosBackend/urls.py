from django.contrib import admin
from django.urls import path, include
from DeimosBackend.endpoints import computational_resources

urlpatterns = [
    path('', include('controller.urls')),
    path('comp_resource', computational_resources),
    path('admin/', admin.site.urls),
]
