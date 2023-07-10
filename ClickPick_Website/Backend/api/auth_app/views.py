from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pymongo import MongoClient
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import User
import jwt
from rest_framework import status
from bson import ObjectId
from api.SingleProduct.models import Product
from api.SingleProduct.serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.mail import EmailMessage
from django.conf import settings
from random import randint

class RegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['favorite_products'] = user.favorite_products

        return token
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        # Update the database here based on successful authentication
        user.last_login = timezone.now()
        user.save()

        token = super().validate(attrs)
        return token

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert birth_date back to a date object if needed
        data['birth_date'] = instance.birth_date
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        # Verify the refresh token
        try:
            refresh = RefreshToken(refresh_token)
            refreshed_token = refresh.access_token
        except:
            return Response({'detail': 'Invalid refresh token.'}, status=400)

        # Check if the refresh token is in the blacklisted_tokens collection
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        blacklisted_tokens = db['blacklisted_tokens']

        if blacklisted_tokens.find_one({'token': refresh_token}):
            return Response({'detail': 'Refresh token is blacklisted.'}, status=400)

        # Add the old refresh token to the blacklisted_tokens collection
        blacklisted_tokens.insert_one({'token': refresh_token})

        response = super().post(request, *args, **kwargs)

        return response
    
class FavoriteProductsListAPIView(APIView):
    permission_classes = (AllowAny,) # Add this line to allow unauthenticated access
    authentication_classes = ()

    def get(self, request):
        token = request.headers.get('Authorization', '').split(" ")[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, algorithms=['HS256'])
            # print(payload['user_id'])
            print('authenticated')
            user_id = payload['user_id']
            user = User.objects.get(id=ObjectId(user_id))

            if user:
                print("User Found")
                serializer = FavoriteProductsSerializer(user)
                return Response(serializer.data)
            else:
                print("User not found")
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

    def post(self, request):
        token = request.headers.get('Authorization', '').split(" ")[1]
        new_product = request.data.get('product_id')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, algorithms=['HS256'])
            # print(payload['user_id'])
            print('authenticated')
            user_id = payload['user_id']
            user = User.objects.get(id=ObjectId(user_id))

            if user:
                favorite_products = user.favorite_products
                print("User Found")
                if new_product in favorite_products:
                    favorite_products.remove(new_product)
                    user.save()
                    return Response({"message": "Product removed successfully."})

                else:
                    favorite_products.append(new_product)
                    user.save()
                    return Response({"message": "Product added successfully."})
            else:
                print("User not found")
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')


class CustomPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 21

class FavMatchingProductsAPIView(APIView):
    permission_classes = (AllowAny,) # Add this line to allow unauthenticated access
    authentication_classes = ()

    def get(self, request):
        token = request.headers.get('Authorization', '').split(" ")[1]
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, algorithms=['HS256'])
            print('authenticated')
            user_id = payload['user_id']
            user = User.objects.get(id=ObjectId(user_id))

            if user:
                print("User Found")
                product_ids = user.favorite_products
                matching_products = Product.objects.filter(ProductID__in=product_ids)

                # Pagination
                paginator = CustomPagination()
                page = paginator.paginate_queryset(matching_products, request)
                serializer = ProductSerializer(page, many=True)

                # Prepare response with pagination metadata
                response_data = {
                    'count': paginator.page.paginator.count,
                    'num_pages': paginator.page.paginator.num_pages,
                    'current_page': paginator.page.number,
                    'products': serializer.data
                }

                return paginator.get_paginated_response(response_data)
            else:
                print("User not found")
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')


class UserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def get(self, request):
        # print(request.headers)
        token = request.headers.get('Authorization', '').split(" ")[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, algorithms=['HS256'])
            # print(payload['user_id'])
            print('authenticated')
            user_id = payload['user_id']
            user = User.objects.get(id=ObjectId(user_id))

            if user:
                print("User Found")
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                print("User not found")
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')


class OTPSendView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):

        get_email = request.data.get('email')
        try:
            user = User.objects.get(email=get_email)
            # Generate and send the OTP
            otp = randint(100000, 999999)
            user.reset_password_otp = otp
            user.save()
            subject = 'Reset Password OTP'
            html_message = f'Your OTP for resetting the password is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [str(user.email)]
            message=EmailMessage(subject,html_message,from_email,to_email)
            message.send()
 
            return Response({'detail': 'OTP sent to the email address.'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'detail': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class OTPCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        get_otp = request.data.get('otp')
        try:
            user = User.objects.get(reset_password_otp=get_otp)
            if user.reset_password_otp is not None:
                return Response(
                    {'detail': 'OTP Verified Successfully.', 'user_id': str(user.id)},
                    status=status.HTTP_200_OK
                )
            else:
                # OTP is null or already used
                return Response({'detail': 'Invalid or Expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # User not found with the given OTP
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            # Handle the case when the OTP is not a valid integer
            return Response({'detail': 'Invalid OTP format.'}, status=status.HTTP_400_BAD_REQUEST)

        
    
class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        get_new_password = request.data.get('new_password')
        get_id=request.data.get('user_id')
        try:
            user = User.objects.get(id=ObjectId(get_id))
            if user.reset_password_otp is not None:
                user.password = make_password(get_new_password)
                user.reset_password_otp = None
                user.save()
                return Response({'detail': 'Password Changes Successfully.'}, status=status.HTTP_200_OK)
            else:
                # OTP is null or already used
                return Response({'detail': 'Invalid or Expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # User not found with the given OTP
            return Response({'detail': 'Invalid UserID.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            # Handle the case when the OTP is not a valid integer
            return Response({'detail': 'Invalid UserID.'}, status=status.HTTP_400_BAD_REQUEST)
        

    # # permission_classes = [AllowAny]
    # def put(self, request):
    #         token=request.headers['Authorization'].split(" ")[1]
    #         if not token:
    #             raise AuthenticationFailed('Unauthenticated!')
    #         try:
    #             payload = jwt.decode(token, algorithms=['HS256'])
    #             print(payload)
    #             print('authenticated')
    #             email_check = "abanoubsamir004@gmail.com"
    #             user = User.objects.filter(email=email_check).first()

    #             if user:
    #                 print(user.full_name)
    #                 new_password = request.data.get('new_password')  # Get the new password from the request data
    #                 if new_password:
    #                     user.password = make_password(new_password)  # Hash the new password
    #                     user.save()
    #                     print("Password updated")
    #                 else:
    #                     print("No new_password provided")
    #             else:
    #                 print("User not found")

    #         except jwt.ExpiredSignatureError:
    #             raise AuthenticationFailed('Unauthenticated!')

    #         user = User.objects.filter(email=email_check).first()
    #         if not user:
    #             raise AuthenticationFailed('User not found!')

    #         serializer = UserSerializer(user)
    #         return Response(serializer.data)
    