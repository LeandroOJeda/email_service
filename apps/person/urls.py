from django.urls import path
from apps.person.views import PersonViewSet

urlpatterns = [
    path(
        "",
        PersonViewSet.as_view({"get": "list", "post": "create"}),
        name="list_persons",
    ),
    path(
        "<int:pk>/",
        PersonViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="detail_of_a_person",
    ),
    path(
        "me/", PersonViewSet.as_view({"get": "retrieve_me"}), name="detail_of_me"),
    path(
        "stats/", PersonViewSet.as_view({"get": "stats"})
    ),
]