from rest_framework.serializers import ModelSerializer
from .models import Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile_picture']

    def create(self, validated_data):
        user = Author.objects.create_user(**validated_data)
        return user


class ResetPasswordSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['password']

        def update(self, instance, validated_data):
            instance.set_password(validated_data['password'])
            instance.save()
            return instance