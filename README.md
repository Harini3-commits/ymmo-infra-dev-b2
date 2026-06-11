# Ymmo — Plateforme de gestion immobilière  
Projet B2 Ynov Informatique — UF INFRA & DEV

## 1. Contexte et objectif

Ymmo est un groupe immobilier basé à Aix-en-Provence avec 12 agences en France.  
L’objectif du projet est de développer une **plateforme web** permettant :

- de gérer un portefeuille de biens immobiliers (vente / location),
- de suivre les clients et les transactions,
- d’analyser les données (prix, villes, chiffre d’affaires),
- d’imaginer une infrastructure réseau d’entreprise adaptée (siège + agences).

Ce dépôt concerne principalement la **partie DEV** : backend FastAPI, base de données, frontend web et script d’analyse.

---

## 2. Fonctionnalités principales

### 2.1. Côté métier / backend

- **Gestion des biens immobiliers** :
  - Création, liste, détail, mise à jour et suppression de biens.
  - Champs : titre, ville, prix, statut, image, adresse, surface, chambres, salles d’eau, type, description, coordonnées GPS.

- **Gestion des clients** :
  - Création, liste, suppression.
  - Champs : nom, prénom, email, téléphone, type (`acheteur` / `vendeur`).

- **Gestion des transactions** :
  - Lien entre un bien et un client.
  - Champs : bien, client, prix de transaction, date, type d’opération (`vente` / `location`), statut.

- **Logique métier sur les statuts** :
  - Lors de la création d’une transaction :
    - si `operation_type = "vente"` ⇒ le bien passe automatiquement en `vendu`,
    - si `operation_type = "location"` ⇒ le bien passe automatiquement en `loue`.
  - Le portefeuille reflète ainsi l’état réel des biens (disponibles, vendus, loués).

- **Statistiques de base** (endpoint `/stats/`) :
  - Nombre total de biens,
  - Répartition simple par statut,
  - Indicateurs globaux.

### 2.2. Côté interface web (frontend)

- **Dashboard d’agent immobilier** :
  - Hero de présentation Ymmo,
  - Colonne carte (Leaflet) avec markers des biens,
  - Colonne formulaire + portefeuille.

- **Formulaire “Ajouter un bien”** :
  - Titre, ville, prix,
  - Adresse complète,
  - Surface, chambres, salles d’eau,
  - Type de bien (appartement, maison, villa, loft, studio…),
  - Statut (`À vendre` / `À louer`),
  - URL de l’image,
  - Latitude / longitude (optionnelles),
  - Description.

- **Portefeuille de biens** :
  - Grille de cartes :
    - photo,
    - titre + adresse,
    - ville + type,
    - surface / chambres / salles d’eau,
    - prix,
    - badge de statut (À vendre, Vendu, À louer, Loué),
    - style différencié pour les biens vendus / loués.

- **Fiche détaillée (modal)** :
  - Ouverture au clic sur une carte,
  - Affichage de la photo en grand, titre, adresse, prix,
  - Description complète (ou message clair si non renseignée),
  - Bloc “Caractéristiques” (surface, chambres, salles d’eau, type),
  - Bloc “Disponibilité” :
    - montre si le bien est disponible ou déjà vendu/loué,
    - cohérent avec le statut de la BDD,
  - Information “Localisation” + recentrage de la carte sur le bien.

- **Carte Leaflet** :
  - Marker par bien :
    - si lat/lng fournis ⇒ position précise,
    - sinon ⇒ position sur la ville.
  - Popup avec titre, prix, statut.
  - Recentrage sur le bien sélectionné depuis la fiche détaillée.

### 2.3. Analyse de données (`analysis.py`)

Le script `analysis.py` analyse la base SQLite `ymmo.db` et affiche dans la console :

- **Biens** :
  - Nombre total de biens,
  - Répartition par statut avec prix moyen,
  - Prix global (min / max / moyen),
  - Prix moyen par ville (top 10),
  - Top 5 villes par nombre de biens,
  - Top 5 biens par surface (titre, ville, surface, prix).

- **Clients** :
  - Nombre total de clients,
  - Répartition par type (`acheteur` / `vendeur`).

- **Transactions** :
  - Nombre total de transactions,
  - Chiffre d’affaires total et prix moyen par transaction (tous types),
  - Chiffre d’affaires uniquement des **ventes** (`operation_type = 'vente'`),
  - Transactions par année (si date au format `YYYY-MM-DD`),
  - Répartition par type d’opération (`vente` / `location`).

Ce script illustre la partie **data / analyse** demandée dans le sujet (exploration des tendances, prix moyens par ville, etc.).

---

## 3. Architecture technique

### 3.1. Backend

- **Framework** : FastAPI (Python).
- **Base de données** : SQLite (`ymmo.db`) via SQLAlchemy.
- **Organisation** :
  - `app/main.py` : création de l’application FastAPI, montage des routers.
  - `app/models.py` : modèles SQLAlchemy (`Property`, `Client`, `Transaction`).
  - `app/schemas.py` : schémas Pydantic (`PropertyCreate`, `PropertyRead`, etc.).
  - `app/routers/` :
    - `properties.py` : routes pour les biens,
    - `clients.py` : routes pour les clients,
    - `transactions.py` : routes pour les transactions,
    - `stats.py` : routes pour les statistiques simples.
  - `app/database.py` : connexion et session DB.
- **API REST** :
  - `/properties/` : CRUD biens,
  - `/clients/` : CRUD clients,
  - `/transactions/` : CRUD transactions + logique métier,
  - `/stats/` : statistiques.

### 3.2. Frontend

- **Technos** : HTML, CSS, JavaScript vanilla.
- **Carte** : Leaflet (OpenStreetMap).
- **Fonctionnement** :
  - `GET /properties/` pour charger les biens,
  - `POST /properties/` pour ajouter un nouveau bien,
  - Rendu dynamique des cartes de biens,
  - Gestion d’un modal de détail,
  - Interaction avec la carte Leaflet.

### 3.3. Analyse

- **Script** : `analysis.py`,
- **Librairie** : `sqlite3` (connexion directe au fichier `ymmo.db`),
- **Usage** : exécuté ponctuellement pour produire un rapport texte en console.

---

## 4. Installation et lancement

### 4.1. Prérequis

- Python 3.10+ recommandé.
- `pip` installé.
- (Optionnel) Machine virtuelle ou environnement local pour la partie INFRA (Windows Server, VMware, etc.).

### 4.2. Cloner le projet

```bash
git clone <URL_DU_REPO>
cd ymmo-infra-dev-b2
```

### 4.3. Créer et activer un environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 4.4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4.5. Lancer l’API FastAPI

```bash
uvicorn app.main:app --reload
```

- API : `http://127.0.0.1:8000`
- Docs Swagger : `http://127.0.0.1:8000/docs`

### 4.6. Lancer le frontend

- Ouvrir `frontend/index.html` dans un navigateur  
  (ou utiliser une extension type “Live Server” de VS Code).
- Vérifier que :
  - les biens s’affichent dans la colonne de droite,
  - les markers apparaissent sur la carte,
  - la fiche détaillée s’ouvre au clic.

### 4.7. Lancer l’analyse de données

```bash
python analysis.py
```

Le script affiche dans la console les statistiques calculées à partir de la base `ymmo.db`.

---

## 5. Utilisation rapide

1. **Créer des biens** :
   - via l’interface web (formulaire “Ajouter un bien”),
   - ou via `/docs` → `POST /properties/`.

2. **Créer des clients** :
   - `/docs` → `POST /clients/`.

3. **Créer des transactions** :
   - `/docs` → `POST /transactions/` avec :
     - `operation_type = "vente"` ou `"location"`,
     - `date` au format `YYYY-MM-DD`.

4. **Vérifier la mise à jour des statuts** :
   - `GET /properties/` → les statuts des biens changent (vendu / loue),
   - sur le site, les badges et la fiche détaillée reflètent ces changements.

5. **Analyser les données** :
   - lancer `analysis.py` pour obtenir les indicateurs (prix moyens, CA, etc.).

---

## 6. Qualité, accessibilité et bonnes pratiques

- **Backend** :
  - séparation claire des responsabilités (modèles, schémas, routers, DB),
  - typage Python et utilisation de Pydantic,
  - statuts gérés côté serveur (pas uniquement côté frontend).

- **Frontend** :
  - design responsive (desktop / tablette / mobile),
  - textes lisibles, contrastes adaptés,
  - labels de formulaires renseignés,
  - feedback utilisateur en cas de succès / erreur (selon la version).

- **Analyse de données** :
  - script dédié,
  - indicateurs directement utiles pour un décideur (prix par ville, CA, statuts).

---

## 7. Partie INFRA (résumé)

La partie INFRA est réalisée sous **VMware** avec :

- une VM **Windows Server** (en cours de promotion en contrôleur de domaine pour le domaine `ymmo.local`, avec rôle AD DS ajouté),
- une configuration réseau en cours de finalisation (IP / DNS à corriger pour terminer la promotion),
- une documentation décrivant :
  - l’installation de Windows Server,
  - l’ajout du rôle Active Directory Domain Services,
  - les problèmes rencontrés au niveau réseau et les pistes de correction.

Une documentation complémentaire (en cours) décrit :

- le **schéma d’architecture réseau** (siège + agences + VPN site-à-site),
- le **plan d’adressage IP**,
- une **politique de sécurité réseau** (pare-feu, filtrage),
- un **plan de sauvegarde et de supervision**,
- une **proposition Cloud** (hébergement de l’API et de la base sur un fournisseur Cloud).

---

## 8. Pistes d’amélioration

- **Côté DEV** :
  - ajouter un endpoint `GET /analysis/` pour exposer les indicateurs de `analysis.py` en JSON,
  - intégrer ces chiffres dans le dashboard (section “Insights”),
  - ajout de filtres de recherche (ville, prix, surface, statut),
  - ajout d’un bouton “Supprimer ce bien” directement dans le frontend,
  - mise en place d’une authentification (agents / admins).

- **Côté INFRA** :
  - finaliser la promotion du contrôleur de domaine,
  - joindre un poste client au domaine,
  - mettre en place un VPN site-à-site simulé entre siège et agence,
  - étendre le schéma à plusieurs agences,
  - automatiser sauvegardes et supervision.

---

## 9. Auteurs

- **Harini Chandracoumar** — Développement backend / frontend / data.
- **Anaïs Ivanov** — Partie INFRA Windows Server / Active Directory et documentation associée.