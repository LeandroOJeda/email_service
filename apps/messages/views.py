
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from apps.utils.multi_smtp_config import FallbackEmailBackend
from django.core.mail.message import EmailMessage
from .models import Message



class MessageViewSet(ModelViewSet):


    def get_serializer_class(self):
        if self.action == "create":
            return MessageSerializer
        


    def create(self, request, *args, **kwargs):

        person_instance = self.request.user
        subject = request.data['subject']
        message = request.data['body']
        from_email = f"{person_instance.first_name}@stagemnes.net.ar"
        to_email = request.data['to_email']
                
        # Envía el correo utilizando la configuración de correo de Django
        email_messages = [EmailMessage(subject, message, from_email, [to_email])]
        email_backend = FallbackEmailBackend()

        try:
            email_backend.send_messages(email_messages)
            Message.objects.create(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to_email=to_email,
                    person= person_instance
                )
            return Response(status=status.HTTP_200_OK, data={'message': 'Correo enviado con éxito.'})
        except Exception as e:
            return Response({'error': str(e)})
