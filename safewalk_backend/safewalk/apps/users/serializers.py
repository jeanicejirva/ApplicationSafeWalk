from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    mot_de_passe = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    mot_de_passe_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'telephone', 'email', 'mot_de_passe', 'mot_de_passe_confirm']

    def validate(self, attrs):
        if attrs['mot_de_passe'] != attrs.pop('mot_de_passe_confirm'):
            raise serializers.ValidationError({"mot_de_passe": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            mot_de_passe=validated_data['mot_de_passe'],
            nom=validated_data['nom'],
            prenom=validated_data.get('prenom'),
            telephone=validated_data.get('telephone'),
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'telephone', 'email', 'date_creation']
        read_only_fields = ['id', 'email', 'date_creation']


class ChangePasswordSerializer(serializers.Serializer):
    ancien_mot_de_passe = serializers.CharField(required=True)
    nouveau_mot_de_passe = serializers.CharField(required=True, validators=[validate_password])
