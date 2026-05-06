from rest_framework import serializers
from .models import ContactConfiance


class ContactConfianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactConfiance
        fields = ['id', 'nom_contact', 'prenom_contact', 'telephone_contact', 'email_contact']
        read_only_fields = ['id']
