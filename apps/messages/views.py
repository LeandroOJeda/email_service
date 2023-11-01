
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import MessageSerializer
from apps.utils.multi_smtp_config import FallbackEmailBackend
from apps.utils.permissions import IsAdministrative
from django.core.mail.message import EmailMessage
from .models import Message
from apps.person.models import Person
from datetime import date



class MessageViewSet(ModelViewSet):


    def get_serializer_class(self):
        if self.action == "create":
            return MessageSerializer
        return MessageSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()
        
        


    def create(self, request, *args, **kwargs):

        person_instance = self.request.user


        # Config variables
        from_email = f"info@stagemnes.net.ar"
        daily_email_limit = 1000

        # Verify the limit email for today
        if person_instance.last_message_date != date.today():
            person_instance.daily_messages = 0
            person_instance.last_message_date = date.today()

        if person_instance.daily_messages >= daily_email_limit:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Has alcanzado el límite diario de mensajes.'})

        subject = request.data['subject']
        message = request.data['body']
        to_email = request.data['to_email']

        # Send email with customs backends
        email_messages = [EmailMessage(subject, message, from_email, [to_email])]
        email_backend = FallbackEmailBackend()

        try:
            email_backend.send_messages(email_messages)
            Message.objects.create(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to_email=to_email,
                    person=person_instance
                )
            # increment the daily email counter
            person_instance.daily_messages += 1
            person_instance.save()

            return Response(status=status.HTTP_200_OK, data={'message': 'Correo enviado con éxito.'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})
        
    
