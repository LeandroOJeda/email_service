from django.urls import path
from apps.roles.views import RoleViewSet


urlpatterns = [
    path(
        "", RoleViewSet.as_view({"post": "create", "get": "list"}), name="list_of_roles"
    ),
    path(
        "<int:pk>/",
        RoleViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="detail_of_a_rol",
    ),
]
