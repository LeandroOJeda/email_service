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
        "change_password/",
        PersonViewSet.as_view({"put": "change_password"}),
        name="change_password_person",
    ),
    path(
        "change_email/",
        PersonViewSet.as_view({"put": "change_email"}),
        name="change_email_person",
    ),
    path("verify_email/", PersonViewSet.as_view({"post": "verify_email"})),
    path(
        "me/", PersonViewSet.as_view({"get": "retrieve_me"}), name="detail_of_me"),
    path(
        "password_reset/",
        PersonViewSet.as_view(
            {"post": "password_reset_request", "put": "password_reset_make"}
        ),
    ),
]