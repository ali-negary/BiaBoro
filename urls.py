from django.urls import re_path

from biaboro.core.views import UserDataView, ApproveRegister

urlpatterns = [
    re_path(r"^users$", UserDataView.as_view(), name="get_all_users"),
    re_path(
        r"^approve$",
        ApproveRegister.as_view(),
        name="approve_user",
    ),
]
