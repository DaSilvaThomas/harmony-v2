# 🎵 Harmony - The Sound of Us

Plateforme communautaire musicale centrée sur la mémoire sonore et les interactions sociales.

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip
- virtualenv (recommandé)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd harmony
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'API Jamendo

1. Créez un compte sur [Jamendo Developer](https://devportal.jamendo.com/)
2. Obtenez votre `CLIENT_ID`
3. Modifiez `harmony/settings.py` ligne 94:
```python
   JAMENDO_CLIENT_ID = 'VOTRE_CLIENT_ID_ICI'
```

### 5. Créer la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Charger les données d'exemple
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 7. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte administrateur.

### 8. Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 9. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le site sera accessible sur: **http://127.0.0.1:8000/**

## 🎯 Accès

- **Site web**: http://127.0.0.1:8000/
- **Administration**: http://127.0.0.1:8000/admin/
  - Username: admin
  - Password: (celui que vous avez créé)

## 📁 Structure du projet
```
harmony/
├── manage.py                    # Script de gestion Django
├── harmony/                     # Configuration principale
│   ├── settings.py             # Paramètres du projet
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuration WSGI
├── accounts/                    # Gestion des utilisateurs
├── salons/                      # Salons musicaux
├── quiz/                        # Mini-jeu quiz
├── notifications/               # Système de notifications
├── core/                        # Pages statiques
├── templates/                   # Templates HTML
├── static/                      # Fichiers statiques (CSS, JS, images)
├── uploads/                     # Fichiers uploadés
└── fixtures/                    # Données d'exemple
```

## 🎨 Fonctionnalités

### ✅ Authentification
- Inscription / Connexion / Déconnexion
- Gestion de profil utilisateur
- Photo de profil et biographie

### ✅ Salons Musicaux
- **Salons Communautaires**: Espaces fixes gérés par les admins
- **Salons Thématiques**: Créés par les utilisateurs
- Chat en temps réel (HTMX polling 3s)
- Lecteur audio partagé
- Système de vote pour les morceaux
- Intégration API Jamendo

### ✅ Quiz Musical
- Thèmes multiples (Pop, Rock, Musiques du monde, OST, Électro)
- Questions texte et audio
- Classement global et par thème
- Mode aléatoire

### ✅ Notifications
- Système de notifications programmées
- Icône clignotante pour nouvelles notifications
- Gestion de l'expiration

### ✅ Design
- Interface sombre (#1a1a1a)
- Palette de couleurs harmonieuse
- TailwindCSS pour le styling
- Responsive design
- Animations et transitions

## 🔧 Technologies utilisées

- **Backend**: Django 5.0
- **Frontend**: HTML5, TailwindCSS (CDN)
- **JavaScript**: HTMX, Alpine.js
- **Base de données**: SQLite3
- **API externe**: Jamendo API
- **Gestion des images**: Pillow

## 📝 Commandes utiles

### Créer une migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### Lancer le serveur
```bash
python manage.py runserver
```

### Publier les notifications (commande personnalisée)
```bash
python manage.py publish_notifications
```

### Créer des données de test
```bash
python manage.py shell
```

Puis dans le shell Python:
```python
from salons.models import Salon, Track
from accounts.models import CustomUser

# Créer un utilisateur
user = CustomUser.objects.create_user('testuser', 'test@example.com', 'password123')

# Créer un salon
salon = Salon.objects.create(
    nom="Test Salon",
    type="thematique",
    description="Un salon de test",
    owner=user
)
```

## 🎮 Utilisation

### 1. Inscription
Créez un compte sur http://127.0.0.1:8000/accounts/register/

### 2. Explorer les salons
Accédez à http://127.0.0.1:8000/salons/ pour voir tous les salons disponibles

### 3. Rejoindre un salon
Cliquez sur un salon pour entrer, discuter et voter pour les morceaux

### 4. Jouer au quiz
Allez sur http://127.0.0.1:8000/quiz/ et choisissez un thème

### 5. Créer un salon thématique
Dans la page des salons, cliquez sur "Créer un salon"

## 🛠️ Administration

Accédez à http://127.0.0.1:8000/admin/ pour:
- Gérer les utilisateurs
- Créer/modifier des salons communautaires
- Ajouter des questions de quiz
- Gérer les notifications
- Modérer les messages

## 🎵 Configuration Jamendo

L'API Jamendo permet de:
- Rechercher des morceaux
- Obtenir des extraits de 30 secondes
- Récupérer les pochettes d'albums
- Accéder à des métadonnées musicales

**Endpoints utilisés**:
- `/tracks/` - Recherche de morceaux

**Paramètres configurés**:
- `client_id`: Votre clé API
- `format`: json
- `audioformat`: mp32 (extraits 30s)

## 🐛 Dépannage

### Problème: Les images ne s'affichent pas
**Solution**: Vérifiez que `MEDIA_ROOT` et `MEDIA_URL` sont configurés dans settings.py

### Problème: HTMX ne fonctionne pas
**Solution**: Vérifiez que le CDN HTMX est accessible dans base.html

### Problème: Erreur API Jamendo
**Solution**: Vérifiez votre `JAMENDO_CLIENT_ID` dans settings.py

### Problème: Migrations échouent
**Solution**: 
```bash
python manage.py makemigrations --empty accounts
python manage.py migrate --fake
```

## 📄 Licence

Ce projet est développé à des fins éducatives.

## 👥 Contact

Pour toute question: contact@harmony-music.com

---

**Harmony** - The Sound of Us 🎵