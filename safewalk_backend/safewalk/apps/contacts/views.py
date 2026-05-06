from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ContactConfiance
from .serializers import ContactConfianceSerializer


class ContactListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/contacts/     — Liste tous les contacts de l'utilisateur connecté.
    POST /api/contacts/     — Ajoute un nouveau contact de confiance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ContactConfianceSerializer

    def get_queryset(self):
        return ContactConfiance.objects.filter(id_users=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id_users=self.request.user)


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/contacts/<id>/ — Détail d'un contact.
    PUT    /api/contacts/<id>/ — Modifier un contact.
    DELETE /api/contacts/<id>/ — Supprimer un contact.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ContactConfianceSerializer

    def get_queryset(self):
        # Un utilisateur ne peut accéder qu'à ses propres contacts
        return ContactConfiance.objects.filter(id_users=self.request.user)
