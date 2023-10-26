import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from apps.person.models import Person
from apps.roles.models import Role
from apps.validation.serializers import CustomTokenObtainPairSerializer
from apps.person.serializers import (
    ChangePasswordPersonSerializer,
    WithRelationsPersonSerializer,
    CreateUpdatePersonSerializer,
    BriefPersonSerializer,
    PersonRolesSerializer,
)
from apps.utils.permissions import IsAdministrative, IsSelf, IsSuperUser, IsTeacher


logger = logging.getLogger()


class PersonViewSet(ModelViewSet):
    search_fields = ["first_name", "last_name", "username", "dni"]
    ordering_fields = ["first_name", "last_name", "username"]
    ordering = ["last_name"]

    def get_serializer_class(self):
        if self.action == "destroy":
            return CreateUpdatePersonSerializer
        elif self.action == "retrieve" or self.action == "retrieve_me":
            return WithRelationsPersonSerializer
        elif self.action == "change_password":
            return ChangePasswordPersonSerializer
        elif self.action == "create" or self.action == "update":
            self.request.action = self.action
            return CreateUpdatePersonSerializer
        elif self.action == "add_role" or self.action == "remove_role":
            return PersonRolesSerializer
        else:
            return BriefPersonSerializer

    def get_permissions(self):
        if self.action in (
            "create",
            "password_reset_request",
            "password_reset_make",
            "activate",
            "verify_email",
            "pre_verify_cuit",
        ):
            self.permission_classes = [AllowAny]
        elif self.action in ("update", "change_password", "retrieve"):
            self.permission_classes = [IsSuperUser | IsSelf]
        elif self.action in "list":
            self.permission_classes = [
                IsSuperUser | IsTeacher | IsAdministrative]
        elif self.action == "destroy":
            self.permission_classes = [IsSuperUser]
        elif self.action in ("add_role", "remove_role"):
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        logger.debug("serializer on perfom create: %s", serializer)
        return Person.objects.create_user(**serializer.validated_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Create token temporary
        token = CustomTokenObtainPairSerializer.get_token(serializer.instance)
        data: dict = WithRelationsPersonSerializer(
            instance=serializer.instance).data
        data["token"] = {"access": str(
            token.access_token), "refresh": str(token)}

        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=["get"], detail=True)
    def retrieve_me(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=self.request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.retrive_me_format_data())

    @action(methods=["put"], detail=True)
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usr = self.request.user
        usr.set_password(serializer.validated_data.get("password_new"))
        usr.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["put"], detail=True)
    def change_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=["post"], detail=True)
    def add_role(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_logged = self.request.user
        user_target = self.get_object()
        if  user_logged.role.level_of_access == 0:
            user_target.roles.add(serializer.validated_data["role"])
            user_target.save()
        return Response(data={user_target.roles.values()}, status=status.HTTP_200_OK)

    @action(methods=["delete"], detail=True)
    def remove_role(self, request, *args, **kwargs):
        new_role = Role.objects.filter(id=kwargs["role"])
        user_logged = self.request.user
        user_target = self.get_object()
        if user_logged.role.level_of_access == 0:
            user_target.roles.remove(new_role.get().id)
            user_target.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


