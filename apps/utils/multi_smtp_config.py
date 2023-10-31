from django.core.mail.backends.smtp import EmailBackend
from os import getenv

class FallbackEmailBackend:
    def __init__(self, *args, **kwargs):
        self.primary_backend = self.create_backend(
            host='smtp.sparkpostmail.com',
            port=587,
            username='SMTP_Injection',
            password=getenv("SPARKPOST_PASSWORD"),
            use_tls=True,
            
        )
        self.secondary_backend = self.create_backend(
            
            host='smtp.elasticemail.com',
            port=2525,
            username='leo170994@gmail.com',
            password=getenv("ELASTICEMAIL_PASSWORD"),
            use_tls=True,

        )

    def create_backend(self, host, port, username, password, use_tls):
        return EmailBackend(
            host=host,
            port=port,
            username=username,
            password=password,
            use_tls=use_tls,
            fail_silently=False,
        )

    def send_messages(self, email_messages):
        for i, backend in enumerate([self.primary_backend, self.secondary_backend], start=1):
            try:
                sent = backend.send_messages(email_messages)
                if sent:
                    print(f"Correo electrónico enviado con éxito utilizando el backend {i}.")
                    return sent
            except Exception as e:
                print(f"Error al enviar el correo electrónico con el backend {i}: {e}")
        print("Todos los backends han fallado.")
        return 0

