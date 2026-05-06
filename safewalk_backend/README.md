# SafeWalk — Backend Django + MySQL

## Structure du projet

```
safewalk_backend/
├── manage.py
├── requirements.txt
├── .env.example
└── safewalk/
    ├── __init__.py
    ├── urls.py
    ├── wsgi.py
    ├── settings/
    │   ├── __init__.py
    │   └── base.py
    └── apps/
        ├── users/          # Inscription, login, profil
        ├── contacts/       # Contacts de confiance
        └── alertes/        # Alertes SOS + contacts notifiés
```

---

## Installation

### 1. Cloner et créer l'environnement virtuel

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec tes vraies valeurs (BDD, secret key…)
```

### 3. Importer la base de données

```bash
mysql -u root -p safewalk < safewalk.sql
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

> Pas besoin de `makemigrations` ni `migrate` : les tables existent déjà via le .sql.
> Si tu veux utiliser `migrate` quand même, lance `python manage.py migrate --fake-initial`.

---

## Endpoints API

Toutes les routes sont préfixées par `/api/`.

### Authentification (JWT)

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/users/register/` | Inscription | Non |
| POST | `/api/users/login/` | Connexion → tokens JWT | Non |
| POST | `/api/users/logout/` | Invalider le refresh token | Oui |
| POST | `/api/auth/refresh/` | Renouveler l'access token | Non |

### Profil utilisateur

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | `/api/users/me/` | Voir son profil | Oui |
| PUT/PATCH | `/api/users/me/` | Modifier son profil | Oui |
| POST | `/api/users/me/password/` | Changer son mot de passe | Oui |

### Contacts de confiance

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | `/api/contacts/` | Lister ses contacts | Oui |
| POST | `/api/contacts/` | Ajouter un contact | Oui |
| GET | `/api/contacts/<id>/` | Détail d'un contact | Oui |
| PUT/PATCH | `/api/contacts/<id>/` | Modifier un contact | Oui |
| DELETE | `/api/contacts/<id>/` | Supprimer un contact | Oui |

### Alertes SOS

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | `/api/alertes/` | Historique des alertes | Oui |
| POST | `/api/alertes/` | Déclencher une alerte | Oui |
| GET | `/api/alertes/<id>/` | Détail d'une alerte | Oui |
| PATCH | `/api/alertes/<id>/resoudre/` | Marquer comme résolue | Oui |
| PATCH | `/api/alertes/<id>/annuler/` | Annuler une alerte | Oui |

---

## Utilisation des tokens JWT

Après login, inclure le token dans chaque requête :

```
Authorization: Bearer <access_token>
```

Renouveler le token expiré :

```http
POST /api/auth/refresh/
{ "refresh": "<refresh_token>" }
```

---

## Exemple — Déclencher une alerte

```http
POST /api/alertes/
Authorization: Bearer <token>
Content-Type: application/json

{
  "latitude": 45.7640,
  "longitude": 4.8357
}
```

Réponse :
```json
{
  "id": 1,
  "latitude": "45.7640000",
  "longitude": "4.8357000",
  "date_alerte": "2026-05-04T10:23:00Z",
  "statut": "active",
  "alertes_contacts": [
    {
      "id": 1,
      "contact": {
        "id": 2,
        "nom_contact": "Dupont",
        "prenom_contact": "Marie",
        "telephone_contact": "0612345678",
        "email_contact": "marie@example.com"
      },
      "statut_envoie": "en_attente"
    }
  ]
}
```

---

## Prochaines étapes suggérées

- **Notifications** : brancher Twilio (SMS) ou SendGrid (email) dans `alertes/views.py` au niveau du `TODO`
- **Tests** : ajouter `pytest-django` et écrire des tests unitaires par app
- **Déploiement** : configurer `gunicorn` + `nginx` pour la prod
