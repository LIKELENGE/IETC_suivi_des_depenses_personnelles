# Procès-Verbal de la Réunion – Projet "La Pécuniaire Magique"

**Date :** 28 Mai 2025  
**Participants :**  
1. Jean Pierre  
2. Harry  
3. Moïse  

---

## Objectif

Mettre en place une architecture fonctionnelle pour l'application **"La Pécuniaire Magique"**, en respectant les contraintes pédagogiques de l'exercice.

---

## Architecture Choisie : MVT (Model - View - Template) avec Flask

L'application adoptera une architecture **Model-View-Template (MVT)**, utilisant le framework **Flask** pour le développement web.

> ⚠️ **Important :** L'utilisation d'une base de données relationnelle est **exclue** pour ce projet.

---

## Composants de l'Architecture

### 1. Modèles (`/models`)
- Contiendront toutes les classes métier de l'application (ex. : `Utilisateur`, `Catégorie`, `Transaction`).
- Intégreront les méthodes métier : **CRUD** (Création, Lecture, Mise à jour, Suppression).
- Une classe générique de base centralisera les opérations communes, telles que la lecture/écriture de fichiers **JSON**.
- Conception orientée objet, avec les principes suivants :
  - **Héritage** : éviter la duplication de code.
  - **Polymorphisme** : permettre des comportements adaptés selon les classes.
  - **Surcharge de méthodes** : adapter les comportements selon les contextes.
  - **Constructeur `__init__`** : pour l'initialisation des objets.

### 2. Routes / Vues (`/views`)
- Gèrent les requêtes HTTP (**GET**, **POST**, etc.).
- Font l'interface entre les modèles et les templates HTML.
- Assurent la **logique de contrôle** :
  - traitement des actions,
  - vérification d'accès,
  - gestion des sessions (connexion/déconnexion).
- Collaborent avec les validateurs de formulaires.

### 3. Validateurs de Formulaires (`/forms`)
- Implémentés avec **WTForms** (ou équivalent).
- Gèrent les formulaires HTML et valident les champs utilisateur.
- Vérifient les **contraintes métier** :
  - formats,
  - champs obligatoires,
  - valeurs numériques, etc.

### 4. Templates (`/templates`)
- Basés sur **Jinja2** pour la génération dynamique des pages HTML.
- Reçoivent les données via les routes.
- Servent de point d’entrée pour les saisies utilisateur et l’affichage des données.

---

## Répartition des Tâches (CRUD par Entité)

| Tâche             | Responsable   |
|------------------|---------------|
| CRUD Utilisateur | Harry         |
| CRUD Catégorie   | Jean-Pierre   |
| CRUD Transaction | Moïse         |
| Formulaires      | Nourridine    |

---

## Contraintes du Projet

- ❌ **Pas de base de données relationnelle**, ni d’ORM.
- ✅ **Stockage via fichiers JSON**.
- 🧱 Application structurée selon les **bonnes pratiques de la POO**, avec séparation claire des responsabilités.

---

## Qualités du Code

- 👓 Lisible
- 🔧 Maintenable
- ✂️ Concis
- 📦 Usage limité de bibliothèques externes, privilégiant :
  - la **facilité d’utilisation**
  - la **richesse fonctionnelle**

---

## Organisation du Travail

- ⏱️ **Sprints de 2 jours**
- ✅ Si une tâche est terminée en avance → aide aux autres
- 🆘 En cas de retard → solliciter de l’aide
- 📅 Réunion de suivi de **15 minutes** après chaque sprint (présentiel ou à distance)
- ⭐ Les **fonctionnalités bonus** ne seront ajoutées **qu’après les fonctionnalités de base**

---
