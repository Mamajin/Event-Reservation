from django.urls import path, include
from stub_api.views import stub_api

urlpatterns = [
    path('', stub_api.urls)
]
