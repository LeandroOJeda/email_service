from django.urls import path
from apps.messages.views import MessageViewSet



urlpatterns = [
    path(
        "", MessageViewSet.as_view({"post": "create"})
    )
]
