from django.urls import path
from .views import AlerteListCreateView, AlerteDetailView, AlerteResolveView, AlerteAnnulerView

urlpatterns = [
    path('', AlerteListCreateView.as_view(), name='alerte-list-create'),
    path('<int:pk>/', AlerteDetailView.as_view(), name='alerte-detail'),
    path('<int:pk>/resoudre/', AlerteResolveView.as_view(), name='alerte-resoudre'),
    path('<int:pk>/annuler/', AlerteAnnulerView.as_view(), name='alerte-annuler'),
]
