import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from django.contrib.auth.tokens import default_token_generator
from apps.person.serializers import WithRelationsPersonSerializer

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        serializer = WithRelationsPersonSerializer(instance=user)

        token["access_level"] = user.role.level_of_access
        token["role"] = serializer.data["role"]
        logger.debug("ROLES FOR TOKEN: %s", token["role"])

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
