from rest_framework import serializers
from .models import User
# from .models import FavoriteProducts

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'birth_date', 'address']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','reset_password_otp','email', 'full_name', 'birth_date', 'address','favorite_products']

class FavoriteProductsSerializer(serializers.Serializer):
    favorite_products = serializers.ListField(child=serializers.CharField())

    def to_representation(self, instance):
        return {'favorite_products': instance.favorite_products}
    


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField(min_value=100000, max_value=999999)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        password = attrs['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Email not found.')

        if user.reset_password_otp != otp:
            raise serializers.ValidationError('Invalid OTP.')

        user.set_password(password)
        user.reset_password_otp = None
        user.save()

        return attrs
