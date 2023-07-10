from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('userView/', UserView.as_view(), name='view-user'),
    path('favoriteList/', FavoriteProductsListAPIView.as_view(), name='favorite-List'),
    path('favMatchingProducts/', FavMatchingProductsAPIView.as_view(), name='user-matching-products'),
    path('sendOTP/', OTPSendView.as_view(), name='reset-password'),
    path('checkOTP/', OTPCheckView.as_view(), name='reset-password'),
    path('resetPassword/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
]
"""
"http://127.0.0.1:8000/api/auth/register/" post all user data (email, full_name, password,birthdate,address) to register
"http://127.0.0.1:8000/api/auth/login/" post  user data (email, password) to login and once it login it post its refresh and access token to the local storage
"http://127.0.0.1:8000/api/auth/token/refresh/" refresh user token and generats a new tokens for security and block the old access token
"http://127.0.0.1:8000/api/auth/userView/" user can veiw its data 
"http://127.0.0.1:8000/api/auth/favoriteList/" user list fav ids
"http://127.0.0.1:8000/api/auth/favMatchingProducts" list and paginate all user fav products that match its list 
"http://127.0.0.1:8000/api/auth/sendOTP/" send an otp to user email
"http://127.0.0.1:8000/api/auth/checkOTP/" verify otp and response with this user_id
"http://127.0.0.1:8000/api/auth/resetPassword/" user can change its password by post {user_id, new_password} where user_id gets when checkOTP

"""