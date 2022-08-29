from django.shortcuts import render
from django.views.decorators.csrf import (
    csrf_exempt,
)  # to allow other domains access to the API
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


from BiaBoro.core.models import (
    UserData,
    UserType,
    Credentials,
    Logins,
    ArrivalDeparture,
)
from BiaBoro.core.serializers import (
    UserDataSerializer,
    UserTypeSerializer,
    CredentialsSerializer,
    LoginsSerializer,
    ArrivalDepartureSerializer,
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
            user_data = UserData.objects.all()
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
            user_data = UserData.objects.filter(**query_without_none)

        # check if user_data is empty
        if user_data:
            # if not empty, serialize the data and return it
            serializer = UserDataSerializer(user_data, many=True)
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
                "ErrorCode": "NoRecordsFound",
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
        # get all records in user_data table matching the query
        query_params = dict(request.query_params)
        get_params = {
            "username": query_params.get("username", None),
            "email": query_params.get("email", None),
        }
        query_without_none = {}
        for key, value in get_params.items():
            if value is not None:
                query_without_none[key] = value[0]
        if query_without_none:
            user_data = UserData.objects.filter(**query_without_none)
            if user_data:
                # if a user is found, continue.
                user_data_ser = UserDataSerializer(user_data, many=True)
                user_data_dict = user_data_ser.data[0]
                user_id = user_data_dict["id"]
                status = query_params.get("status", None)
                if status is not None:
                    status = status[0]
                    if status in ["True", "False"]:
                        user_credentials = Credentials.objects.get(user=user_id)
                        user_credentials.active = True if status == "True" else False
                        user_credentials.save()
                        response_message = (
                            "Registration is approved."
                            if status == "True"
                            else "Registration is denied."
                        )
                        return JsonResponse(
                            {
                                "message": response_message,
                                "data": query_without_none,
                            },
                            status=200,
                        )

                return JsonResponse(
                    {
                        "message": "Enter Status or Set its value to True or False",
                        "ErrorCode": "InvalidQueryParameters",
                        "data": [],
                    },
                    status=400,
                )

            return JsonResponse(
                {
                    "message": "Unable to find user with specified info",
                    "ErrorCode": "NoRecordsFound",
                    "data": [],
                },
                status=404,
            )

        return JsonResponse(
            {
                "message": "Enter either Username or Email",
                "ErrorCode": "InvalidQueryParameters",
                "data": [],
            },
            status=400,
        )
