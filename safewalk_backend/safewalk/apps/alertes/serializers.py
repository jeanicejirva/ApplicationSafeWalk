from rest_framework import serializers
from .models import Alerte, AlerteContact
from safewalk.apps.contacts.serializers import ContactConfianceSerializer


class AlerteContactSerializer(serializers.ModelSerializer):
    contact = ContactConfianceSerializer(source='contacts', read_only=True)

    class Meta:
        model = AlerteContact
        fields = ['id', 'contact', 'statut_envoie']


class AlerteSerializer(serializers.ModelSerializer):
    alertes_contacts = AlerteContactSerializer(many=True, read_only=True)

    class Meta:
        model = Alerte
        fields = ['id', 'latitude', 'longitude', 'date_alerte', 'statut', 'alertes_contacts']
        read_only_fields = ['id', 'date_alerte', 'alertes_contacts']


class AlerteCreateSerializer(serializers.ModelSerializer):
    """Serializer utilisé à la création : accepte lat/lon et déclenche les notifications."""

    class Meta:
        model = Alerte
        fields = ['latitude', 'longitude', 'statut']
        extra_kwargs = {'statut': {'required': False}}
