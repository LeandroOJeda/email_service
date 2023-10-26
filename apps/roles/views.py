from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
# from apps.utils.permissions import IsAdministrative, IsSuperUser
from apps.roles.serializers import RoleSerializer, RoleCreateSerializer
from apps.roles.models import Role


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "destroy"):
            return RoleSerializer
        else:
            return RoleCreateSerializer
