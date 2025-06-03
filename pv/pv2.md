# PV de la Réunion – 28 Mai 2025  
## Projet : Création d’une application de suivi de dépenses personnelles – *La Pécuniaire Magique*

---

### 👥 Participants

1. Jean Pierre  
2. Harry  
3. Moïse  

---

### 🎯 Objectif

Se mettre d’accord sur une **architecture fonctionnelle** pour l’application *La Pécuniaire Magique*, en respectant les **contraintes pédagogiques** de l’exercice, ainsi que la **répartition des tâches** pour une collaboration optimale où chacun participe activement.

---

### 🧱 Décisions sur l'Architecture

- **Architecture choisie** :  (*Model – Route – Template*), à condition qu’elle soit **validée par M. Burniaux** (le client).
- **Architecture alternative** : Passage à **Tkinter** si l’option flask est refusée.

---

### ⚙️ Architecture retenue 

L'application sera développée avec le **framework Flask**, en **excluant l’usage d’une base de données relationnelle**.

---

### 🔧 Composants de l’Application

#### 📦 Modèles (Models)
- Représentation des entités : `Utilisateur`, `Catégorie_dépense`, `Transaction`.
- Méthodes CRUD et logique métier intégrées.
- Création d'une **classe de base générique** pour :
  - Lecture/écriture de fichiers JSON.
  - Mutualisation du code.
- Concepts POO utilisés : héritage, polymorphisme, surcharge, constructeurs.

#### 🌐 Routes 
- Gestion des requêtes HTTP (`GET`, `POST`).
- Gestion des sessions utilisateur (connexion, déconnexion).
- Lien entre modèles et templates.

#### 📝 Templates
- Utilisation de **Jinja2**.
- Affichage des données et interfaces de saisie dynamiques.

#### ✅ Validateurs de Formulaires
- Utilisation de **WTForms** (ou équivalent).
- Validation métier des champs saisis.

---

### 👨‍💻 Répartition des Tâches

| Fonctionnalité                 | Responsable   |
|-------------------------------|---------------|
| CRUD Utilisateur              | Harry         |
| CRUD Catégorie                | Jean Pierre   |
| CRUD Transaction              | Moïse         |
| Validateurs de formulaires    | Nourredine    |

---

### 📌 Contraintes du Projet

- **Pas de base de données relationnelle** (pas de SQL, pas d’ORM).
- Données stockées sous **format JSON**.
- Application structurée selon les **principes de la POO**.
- **Séparation claire des responsabilités**.

---

### ✅ Qualités attendues du Code

- Lisibilité, maintenabilité, concision.
- Usage **limité et justifié** de bibliothèques externes.

---

### 🗓️ Organisation du Travail

- **Sprints de 2 jours**.
- **Réunions de suivi** de 15 minutes après chaque sprint.
- Entraide encouragée entre membres de l’équipe.
- Développement de **fonctionnalités bonus uniquement après finalisation du socle fonctionnel**.

---

