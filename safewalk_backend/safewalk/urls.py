from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('safewalk.apps.users.urls')),
    path('api/contacts/', include('safewalk.apps.contacts.urls')),
    path('api/alertes/', include('safewalk.apps.alertes.urls')),
]
