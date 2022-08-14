from django.urls import re_path

from BiaBoro.core.views import UserDataView

urlpatterns = [
    re_path(r"^users$", UserDataView.as_view(), name="all_users"),
    re_path(r"^users(?P<pk>[0-9]+)$", UserDataView.as_view(), name="filter_users"),
]
