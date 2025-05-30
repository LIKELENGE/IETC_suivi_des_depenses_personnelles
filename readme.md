# 💸 La Pécuniaire Magique

**Une application de gestion financière simple, pédagogique et 100% JSON.**

---

## 📌 Objectif du Projet

Développer une application web de gestion de transactions personnelles, à visée pédagogique, sans base de données relationnelle. Le projet met l'accent sur la séparation des responsabilités, la programmation orientée objet (POO), et l'architecture MVT avec Flask.

---

## 🧱 Architecture

### 🔄 Modèle - Vue - Template (MVT) avec Flask

| Composant      | Rôle                                                                 |
|----------------|----------------------------------------------------------------------|
| **Models**     | Gestion des entités métier (Utilisateur, Catégorie, Transaction) et logique métier (CRUD via fichiers JSON) |
| **Views (Routes)**  | Traitement des requêtes HTTP, logique de contrôle et gestion des sessions |
| **Forms**       | Validation des données utilisateurs via WTForms                     |
| **Templates**   | Génération dynamique des pages avec Jinja2                          |

---

## 📂 Structure du Projet