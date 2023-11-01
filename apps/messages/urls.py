from django.urls import path
from apps.messages.views import MessageViewSet



urlpatterns = [
    path(
        "send_mail/", MessageViewSet.as_view({"post": "create"})
    ),
]
