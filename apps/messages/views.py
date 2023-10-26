from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import MessageSerializer


class MessageViewSet(ModelViewSet):


    def get_serializer_class(self):
        if self.action == "create":
            return MessageSerializer
