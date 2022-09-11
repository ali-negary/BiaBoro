import logging
from datetime import timedelta

import django.db.utils
from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import (
    csrf_exempt,
)  # to allow other domains access to the API
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


from BiaBoro.core.models import (
    Employee,
    UserType,
    LoginLogout,
    ArrivalDeparture,
)
from BiaBoro.core.serializers import (
    EmployeeSerializer,
    UserTypeSerializer,
    LoginLogoutSerializer,
    ArrivalDepartureSerializer,
    RegisterSerializer,
)


class UserDataView(APIView):
    """
    This view is used to handle all requests related to users.
    """

    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        # get all records in user_data table matching the query
        query_params = dict(request.query_params)
        if not query_params:
            # get all the records in user_data table
            user_data = Employee.objects.all()
        else:
            # get the records that match the query parameters
            query_params = {
                "first_name": query_params.get("first_name", None),
                "last_name": query_params.get("last_name", None),
                "email": query_params.get("email", None),
                "national_id_number": query_params.get("national_id_number", None),
                "contract_type": query_params.get("contract_type", None),
                "user_role": query_params.get("user_role", None),
                "username": query_params.get("username", None),
            }
            query_without_none = {}
            for key, value in query_params.items():
                if value is not None:
                    value = value[0]
                    if "," in value:
                        # use __in filter if there are multiple values
                        query_without_none[key + "__in"] = value.split(",")
                    else:
                        query_without_none[key] = value
            user_data = Employee.objects.filter(**query_without_none)

        # check if user_data is empty
        if user_data:
            # if not empty, serialize the data and return it
            serializer = EmployeeSerializer(user_data, many=True)
            return JsonResponse(
                {
                    "message": f"Users Found",
                    "records_count": len(serializer.data),
                    "data": serializer.data,
                },
                status=200,
                safe=False,
            )
            # safe=False is for allowing the data to be returned in JSON format
            # even if it is not safe.
        return JsonResponse(
            {
                "message": "Unable to find user with specified info",
                "ErrorCode": "NoRecordFound",
                "data": [],
            },
            status=404,
        )


class ApproveRegister(APIView):
    """
    This class is used to approve registration of direct-reports.
    """

    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def patch(self, request):
        username = request.query_params.get("username", None)
        user_status = request.query_params.get("status", None)
        if (username is not None) and (user_status is not None):
            try:
                user = User.objects.get(username=username)
                user_status = True if user_status.lower() == "approve" else False
                user.is_active = user_status
                user.save()
                response_message = (
                    "User activated." if user_status else "User deactivated."
                )
                return JsonResponse(
                    {
                        "message": response_message,
                        "data": {"username": username},
                    },
                    status=200,
                )
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        "message": (
                            f"Unable to find user with specified info "
                            f"(username:'{username}').",
                        ),
                        "ErrorCode": "NoRecordFound",
                    },
                    status=404,
                )
        return JsonResponse(
            {
                "message": "Enter Username and Status",
                "ErrorCode": "InvalidQueryParameters",
                "data": [],
            },
            status=400,
        )


class UserRegister(APIView):
    """This class handles the registration process."""

    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        serializer = RegisterSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    "message": f"New user '{serializer.data['username']}' is registered.",
                },
                status=200,
            )
        return JsonResponse(
            {
                "message": serializer.errors,
                "ErrorCode": "RegistrationFailed",
            },
            status=401,
        )


class UserLogin(APIView):
    """This class handles login requests."""

    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        AllowAny,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        login_time = timezone.now()
        body = request.data
        username = body.get("username", "")
        if username:
            password = body.get("password", "")
            if password:
                user = User.objects.get(username=username)
                check_result = user.check_password(raw_password=password)
                if check_result:
                    is_logged_in = ""
                    try:
                        user_token = Token.objects.get(user_id=user.id)
                        is_logged_in = "is already"
                        logging.info(f'User "{username}" is already logged in.')
                    except Token.DoesNotExist:
                        user_token = Token.objects.create(user=user)
                        logging.info(f'User "{username}" logged in.')
                        # update the last_login
                        user.last_login = login_time
                        user.save()
                        # add new record to login_logout
                        login = LoginLogout(
                            record_date=login_time, record_type="login", user_id=user.id
                        )
                        login.save()
                    return JsonResponse(
                        {
                            "message": f"User '{username}' {is_logged_in} logged in.",
                            "data": {"token": user_token.key},
                        },
                        status=200,
                    )

                return JsonResponse(
                    {
                        "message": "Password does not match",
                        "ErrorCode": "InvalidPassword",
                    },
                    status=401,
                )

            return JsonResponse(
                {
                    "message": "Enter password.",
                    "ErrorCode": "InvalidQueryParameters",
                },
                status=400,
            )

        return JsonResponse(
            {
                "message": "Enter username.",
                "ErrorCode": "InvalidQueryParameters",
            },
            status=400,
        )


class UserLogout(APIView):
    """This class handles login requests."""

    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        user = request.user
        user_id = user.id
        Token.objects.get(user_id=user_id).delete()
        # add new record to login_logout
        logout_time = timezone.now()
        logout = LoginLogout(
            record_date=logout_time, record_type="logout", user_id=user.id
        )
        logout.save()
        return JsonResponse(
            {
                "message": f"User '{user.username}' is logged out.",
                "ErrorCode": "UserLoggedOut",
            },
            status=200,
        )
