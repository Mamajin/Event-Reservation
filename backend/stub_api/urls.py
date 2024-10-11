from django.urls import path,include
from .views import stub_api

urlpatterns = [
    path('stub_api/', stub_api.urls)
]
