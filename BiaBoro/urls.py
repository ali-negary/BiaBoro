"""BiaBoro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the 'include()' function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include

from BiaBoro.core.views import *

urlpatterns = [
    re_path(r"^api/user/info$", UserDataView.as_view(), name="get_all_users"),
    re_path(r"^api/user/register$", UserRegister.as_view(), name="register_user"),
    re_path(r"^api/user/login$", UserLogin.as_view(), name="login_user"),
    re_path(r"^api/user/logout$", UserLogout.as_view(), name="logout_user"),
    re_path(
        r"^api/user/approve$",
        ApproveRegister.as_view(),
        name="approve_user",
    ),
]
