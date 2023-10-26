from django.core.mail.backends.smtp import EmailBackend
from os import getenv


class FallbackEmailBackend:
    def __init__(self, *args, **kwargs):

        # SendGrid SMTP config
        self.primary_backend = EmailBackend(
            host='smtp.elasticemail.com',
            port=2525,
            username='leo170994@gmail.com',
            password= getenv("ELASTICE_PASSWORD"),
            use_tls=True,
            fail_silently=False,
        )

        # SparkPost SMTP config
        self.secondary_backend = EmailBackend(
            host='smtp.sparkpostmail.com',
            port=587,
            username='SMTP_Injection',
            password=getenv("SPARKPOST_PASSWORD"),
            use_tls=True,
            fail_silently=False,
        )

    def send_messages(self, email_messages):
        try:
            return self.primary_backend.send_messages(email_messages)
        except Exception as e:
            print(f"Error sending email with primary backend: {e}")
            return self.secondary_backend.send_messages(email_messages)