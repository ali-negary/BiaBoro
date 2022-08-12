from django.shortcuts import render
from django.views.decorators.csrf import (
    csrf_exempt,
)  # to allow other domains access to the API
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

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


@csrf_exempt
def user_data_api_list(request):
    """
    This view is used to handle all requests to the UserData API.
    """
    if request.method == "GET":
        # get all the records in user_data table
        user_data = UserData.objects.all()
        # check if user_data is empty
        if user_data:
            # if not empty, serialize the data and return it
            serializer = UserDataSerializer(user_data, many=True)
            return JsonResponse(
                {"message": "Users Found", "data": serializer.data},
                status=200,
                safe=False,
            )
            # safe=False is for allowing the data to be returned in JSON format
            # even if it is not safe.
        return JsonResponse({"message": "No records found", "data": []}, status=404)

    elif request.method == "POST":
        # create a new record in user_data table
        data = JSONParser().parse(request)
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "PUT":
        # update a record in user_data table
        data = JSONParser().parse(request)
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
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
