from rest_framework import serializers
from .models import UserData, UserType, Credentials, Logins, ArrivalDeparture


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = "__all__"


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = "__all__"


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = "__all__"


class LoginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logins
        fields = "__all__"


class ArrivalDepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalDeparture
        fields = "__all__"
