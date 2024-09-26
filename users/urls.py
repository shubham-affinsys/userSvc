from django.urls import path
from .views import *

urlpatterns = [
    path("",all_users,name="allusers"),
    path("addUser/",add_user,name="add-user"),
]
