# Rapport Synthétique - Application de Gestion des Projections de Films

## Introduction
Cette application web permet aux cinémas parisiens de gérer leur programmation de films et aux utilisateurs de consulter les films à l'affiche. Elle est construite selon une architecture MVC (Modèle-Vue-Contrôleur) en utilisant le framework Flask.

## Schémas Fonctionnels

### Architecture Globale

```mermaid
graph TB
    subgraph "Frontend"
        UI[Interface Utilisateur]
        Templates[Templates Jinja2]
        Bootstrap[Bootstrap + FontAwesome]
    end

    subgraph "Backend (Flask)"
        Routes[Routes Controller]
        Auth[Authentication Manager]
        Session[Session Manager]
    end

    subgraph "Base de Données"
        Models[Models ORM]
        SQLite[(SQLite DB)]
    end

    subgraph "Utilisateurs"
        Public[Utilisateur Public]
        Cinema[Cinéma Authentifié]
    end

    %% Connexions Frontend
    UI --> Templates
    Templates --> Bootstrap
    
    %% Connexions Backend
    Routes --> Auth
    Routes --> Session
    Routes --> Models
    Auth --> Session
    
    %% Connexions Base de Données
    Models --> SQLite
    
    %% Flux Utilisateurs
    Public --> UI
    Cinema --> UI
    
    %% Flux de Données
    UI <--> Routes
    Templates <--> Routes

    %% Légende des interactions
    classDef frontend fill:#f9f,stroke:#333,stroke-width:2px
    classDef backend fill:#bbf,stroke:#333,stroke-width:2px
    classDef database fill:#bfb,stroke:#333,stroke-width:2px
    classDef users fill:#fbb,stroke:#333,stroke-width:2px
    
    class UI,Templates,Bootstrap frontend
    class Routes,Auth,Session backend
    class Models,SQLite database
    class Public,Cinema users
```

### Flux des Cas d'Utilisation

```mermaid
sequenceDiagram
    participant U as Utilisateur Public
    participant C as Cinéma
    participant F as Frontend
    participant R as Routes
    participant DB as Base de Données

    %% Cas 1: Consultation des films
    U->>F: Consulte les films par ville
    F->>R: GET /movies/<ville>
    R->>DB: Query films & séances
    DB-->>R: Résultats
    R-->>F: Données formatées
    F-->>U: Affichage des films

    %% Cas 2: Authentification Cinéma
    C->>F: Login (email/password)
    F->>R: POST /login
    R->>DB: Vérification credentials
    DB-->>R: Validation
    R-->>F: Session token
    F-->>C: Accès Dashboard

    %% Cas 3: Ajout d'un film
    C->>F: Ajoute un nouveau film
    F->>R: POST /cinema/dashboard
    R->>DB: Insert film & séances
    DB-->>R: Confirmation
    R-->>F: Succès
    F-->>C: Film ajouté
```

## Architecture Technique

### 1. Structure du Projet
```
projet_rest/
├── app/                      # Package principal de l'application
│   ├── __init__.py          # Initialisation de l'application et des extensions
│   ├── models.py            # Modèles de données (ORM)
│   ├── routes.py            # Contrôleurs et points d'entrée API
│   ├── templates/           # Vues (templates Jinja2)
│   └── static/              # Fichiers statiques
├── venv/                    # Environnement virtuel Python
├── requirements.txt         # Dépendances du projet
├── .env                     # Variables d'environnement
└── README.md               
```

### 2. Composants Principaux

#### 2.1 Backend (Python/Flask)
- **Application Core** (`__init__.py`)
  - Configuration de l'application Flask
  - Initialisation de la base de données
  - Gestion de l'authentification
  - Configuration des variables d'environnement

- **Modèles de Données** (`models.py`)
  - `Cinema`: Gestion des informations des cinémas et authentification
  - `Movie`: Stockage des informations des films
  - `MovieSchedule`: Gestion des programmations et séances

- **Contrôleurs** (`routes.py`)
  - API REST pour la gestion des films
  - Endpoints pour l'authentification
  - Routes pour l'affichage des vues

#### 2.2 Frontend
- **Templates** (Jinja2 + Bootstrap 5)
  - `base.html`: Template de base avec navigation
  - `index.html`: Page d'accueil
  - `cinema_dashboard.html`: Interface d'administration des cinémas
  - `movie_list.html`: Liste des films par ville
  - `movie_details.html`: Détails d'un film
  - `login.html`: Page de connexion

### 3. Technologies Utilisées

#### 3.1 Backend
- **Flask** (v3.1.0)
  - Framework web léger et modulaire
  - Routing des requêtes HTTP
  - Gestion des sessions

- **SQLAlchemy** (v3.1.1)
  - ORM pour la gestion de la base de données
  - Mapping objet-relationnel
  - Abstraction de la base de données

- **Flask-Login** (v0.6.3)
  - Gestion de l'authentification
  - Sessions utilisateur
  - Protection des routes

#### 3.2 Frontend
- **Bootstrap** (v5.3.0)
  - Framework CSS responsive
  - Composants d'interface utilisateur
  - Grille flexible

- **Font Awesome** (v6.0.0)
  - Icônes vectorielles
  - Amélioration de l'interface utilisateur

#### 3.3 Base de Données
- **SQLite**
  - Base de données légère
  - Stockage local
  - Pas de configuration serveur nécessaire

### 4. Fonctionnalités Implémentées

#### 4.1 Espace Public
- Consultation des films par ville
- Affichage détaillé des informations des films
- Vue des horaires et lieux de projection
- Interface responsive et moderne

#### 4.2 Espace Cinéma (Authentifié)
- Système d'authentification sécurisé
- Gestion des films (ajout, programmation)
- Dashboard personnalisé
- Gestion des séances (dates, horaires, jours)

### 5. Sécurité
- Hachage des mots de passe avec Werkzeug
- Protection CSRF sur les formulaires
- Sessions sécurisées
- Variables d'environnement pour les données sensibles

### 6. Points d'Extension Possibles
- API REST complète pour l'intégration avec d'autres services
- Système de réservation de billets
- Gestion des images des films
- Système de notation et commentaires
- Internationalisation (i18n)

## Conclusion
L'application a été conçue avec une architecture modulaire et évolutive, permettant une maintenance facile et des extensions futures. L'utilisation de technologies modernes assure une expérience utilisateur optimale tout en maintenant une base de code propre et maintenable.