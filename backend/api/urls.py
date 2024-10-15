from django.urls import path,include
from api.views import api



urlpatterns = [
    path('', api.urls)
]
