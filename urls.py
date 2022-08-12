from django.urls import re_path

from BiaBoro.core.views import (
    user_data_api_list,
)

urlpatterns = [
    re_path(r"^users$", user_data_api_list),
    re_path(r"^users/(?P<pk>[0-9]+)$", user_data_api_list),
]
