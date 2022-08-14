from django.shortcuts import render
from django.views.decorators.csrf import (
    csrf_exempt,
)  # to allow other domains access to the API
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queryset = UserData.objects.none()

    def get(self, request):
        # get all records in user_data table matching the query
        query_params = dict(request.GET)
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
        return JsonResponse({"message": "No Records Found", "data": []}, status=404)

    def post(self, request):
        # create a record in user_data table
        data = JSONParser().parse(request)
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request):
        # update a record in user_data table
        data = JSONParser().parse(request)
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request):
        # delete a record in user_data table
        data = JSONParser().parse(request)
        email = data.get("email", None)
        national_id_number = data.get("national_id_number", None)
        user = UserData.objects.filter(
            email=email, national_id_number=national_id_number
        )
        user_serializer = UserDataSerializer(data=user)
        if user_serializer.is_valid():
            user.delete()
            return JsonResponse(user_serializer.data, status=201)
        return JsonResponse(user_serializer.errors, status=400)
