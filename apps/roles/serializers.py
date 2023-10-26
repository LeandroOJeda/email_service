from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"


class RoleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = "__all__"
