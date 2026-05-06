from django.db import models
from django.conf import settings


class ContactConfiance(models.Model):
    id_users = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_users',
        related_name='contacts'
    )
    nom_contact = models.CharField(max_length=100)
    prenom_contact = models.CharField(max_length=100)
    telephone_contact = models.CharField(max_length=20)
    email_contact = models.EmailField(max_length=150)

    class Meta:
        db_table = 'contacts_confiance'
        verbose_name = 'Contact de confiance'

    def __str__(self):
        return f"{self.prenom_contact} {self.nom_contact}"
