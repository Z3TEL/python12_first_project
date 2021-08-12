from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(required=True)
    kast_name = serializers.CharField(required=False)


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise  serializers.ValidationError("Пользоваатель с таким email уже зарегистрирован")
        return email

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пороли должны совподать')
        return data


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        user.send_activation_email()
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    # def validate_email(self, email):
    #     if not User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError("Пользователь ненайден")
    #     return email
    #
    # def validate(self, code):
    #     if not User.objects.filter(activation_code=code).exists():
    #         raise serializers.ValidationError("Пользователь ненайден")
    #     return code


    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Пользователь ненайден')
        return data

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    pass


class ForgotPasswordSerializer(serializers.Serializer):
    pass


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь ненайден")
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError("Неверный email и пороль")
        else:
            raise serializers.ValidationError("Email и пороль обезательные")
        data['user'] = user
        return data