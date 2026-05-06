from django.db import models
from django.conf import settings
from safewalk.apps.contacts.models import ContactConfiance


class Alerte(models.Model):
    class Statut(models.TextChoices):
        ACTIVE = 'active', 'Active'
        RESOLUE = 'resolue', 'Résolue'
        ANNULEE = 'annulee', 'Annulée'

    id_users = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column='id_users',
        related_name='alertes'
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    date_alerte = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=Statut.choices, default=Statut.ACTIVE)

    class Meta:
        db_table = 'alertes'
        ordering = ['-date_alerte']
        verbose_name = 'Alerte'

    def __str__(self):
        return f"Alerte #{self.id} — {self.statut} ({self.date_alerte:%d/%m/%Y %H:%M})"


class AlerteContact(models.Model):
    class StatutEnvoie(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        ENVOYE = 'envoye', 'Envoyé'
        ECHEC = 'echec', 'Échec'

    alertes = models.ForeignKey(
        Alerte,
        on_delete=models.RESTRICT,
        db_column='alertes_id',
        related_name='alertes_contacts'
    )
    contacts = models.ForeignKey(
        ContactConfiance,
        on_delete=models.RESTRICT,
        db_column='contacts_id',
        related_name='alertes_contacts'
    )
    statut_envoie = models.CharField(
        max_length=50,
        choices=StatutEnvoie.choices,
        default=StatutEnvoie.EN_ATTENTE
    )

    class Meta:
        db_table = 'alertes_contacts'
        verbose_name = 'Alerte-Contact'

    def __str__(self):
        return f"Alerte #{self.alertes_id} → Contact #{self.contacts_id} ({self.statut_envoie})"
