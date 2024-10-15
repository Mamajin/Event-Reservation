<<<<<<< HEAD
from django.urls import path, include
from api.views import api

=======
from django.urls import path,include
from api.views import api



>>>>>>> ef1db1d455e6a45baa7ca3ce2e4a3e509f8f2337
urlpatterns = [
    path('', api.urls)
]
