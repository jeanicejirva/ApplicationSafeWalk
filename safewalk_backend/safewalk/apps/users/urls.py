from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ChangePasswordView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('me/', ProfileView.as_view(), name='user-profile'),
    path('me/password/', ChangePasswordView.as_view(), name='user-change-password'),
]
