from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginView, name="login"),
    path("register", views.register, name="register"),
    path("myblogs", views.myblogs, name="myblogs"),
    path("addblog", views.addblog, name="addblog"),
    path("logout", views.logoutView, name="logout"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("delete", views.delete, name="delete"),
]
