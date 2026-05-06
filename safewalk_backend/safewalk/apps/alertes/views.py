from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Alerte, AlerteContact
from .serializers import AlerteSerializer, AlerteCreateSerializer
from safewalk.apps.contacts.models import ContactConfiance


class AlerteListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/alertes/  — Historique des alertes de l'utilisateur connecté.
    POST /api/alertes/  — Déclencher une nouvelle alerte (notifie tous les contacts).
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AlerteCreateSerializer
        return AlerteSerializer

    def get_queryset(self):
        return Alerte.objects.filter(id_users=self.request.user).prefetch_related(
            'alertes_contacts__contacts'
        )

    def perform_create(self, serializer):
        alerte = serializer.save(id_users=self.request.user)
        # Créer une entrée AlerteContact pour chaque contact de confiance
        contacts = ContactConfiance.objects.filter(id_users=self.request.user)
        AlerteContact.objects.bulk_create([
            AlerteContact(alertes=alerte, contacts=contact, statut_envoie='en_attente')
            for contact in contacts
        ])
        # TODO : brancher ici l'envoi de SMS/email via un service externe (ex: Twilio, SendGrid)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Retourner l'alerte complète avec ses contacts
        alerte = Alerte.objects.prefetch_related('alertes_contacts__contacts').get(
            pk=serializer.instance.pk
        )
        return Response(AlerteSerializer(alerte).data, status=status.HTTP_201_CREATED)


class AlerteDetailView(generics.RetrieveAPIView):
    """GET /api/alertes/<id>/ — Détail d'une alerte avec ses contacts notifiés."""
    permission_classes = [IsAuthenticated]
    serializer_class = AlerteSerializer

    def get_queryset(self):
        return Alerte.objects.filter(id_users=self.request.user).prefetch_related(
            'alertes_contacts__contacts'
        )


class AlerteResolveView(APIView):
    """PATCH /api/alertes/<id>/resoudre/ — Marquer une alerte comme résolue."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        alerte = get_object_or_404(Alerte, pk=pk, id_users=request.user)
        if alerte.statut != Alerte.Statut.ACTIVE:
            return Response(
                {'detail': "Seule une alerte active peut être résolue."},
                status=status.HTTP_400_BAD_REQUEST
            )
        alerte.statut = Alerte.Statut.RESOLUE
        alerte.save()
        return Response(AlerteSerializer(alerte).data)


class AlerteAnnulerView(APIView):
    """PATCH /api/alertes/<id>/annuler/ — Annuler une alerte active."""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        alerte = get_object_or_404(Alerte, pk=pk, id_users=request.user)
        if alerte.statut != Alerte.Statut.ACTIVE:
            return Response(
                {'detail': "Seule une alerte active peut être annulée."},
                status=status.HTTP_400_BAD_REQUEST
            )
        alerte.statut = Alerte.Statut.ANNULEE
        alerte.save()
        return Response(AlerteSerializer(alerte).data)
