
# 💸 La Pécuniaire Magique

**Une application pédagogique de gestion de finances personnelles, construite avec Flask, sans base de données relationnelle.**

---

## 📌 Objectif du Projet

Développer une application permettant la gestion de transactions (revenus/dépenses), en respectant les bonnes pratiques de la programmation orientée objet et en stockant les données dans des fichiers JSON.

---

## 👥 Membres de l'équipe

- **MarcelVermeulen536**
- **LIKELENGE**
- **ietc-JPierre**
- **Ajsama Abiel-Jason** 

---

## 🧱 Architecture

| Composant      | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **Models**     | Contiennent les classes métier : `Utilisateur`, `Catégorie`, `Transaction`. Opérations CRUD via fichiers JSON, orientées objet. |
| **views**      | Gèrent les routes Flask (GET/POST), la logique de contrôle et les sessions. |
| **Forms**      | Validation des données utilisateurs via WTForms.                            |
| **Templates**  | Génération des pages HTML avec Jinja2.                                      |

---

## 📂 Structure du Projet

```
la-pecuniaire-magique/
│
├── models/             # Modèles métier (POO + JSON)
│   ├── classe_generique.py         # Classe mère avec logique de persistance
│   ├── utilisateur.py
│   ├── statistique_financiere.py 
│   ├── categorie_depense.py
│   └── transaction.py
│
├── views/              
│   └── personne_view.py
│   └── depense_view.py
│   └── revenu_view.py
│   └── categorie_depense_view.py
│
├── forms/              # Formulaires et validation
│   └── forms.py
│
├── templates/          # Fichiers HTML Jinja2
│   └── ...
│
├── static/             # Fichiers CSS, JS ou images (si nécessaire)
│
├── data/               # Données persistées au format JSON
│   ├── utilisateurs.json
│   ├── depenses.json
│   ├── revenus.json
│   ├── categories.json
│   └── transactions.json
│
├── app.py              # Point d’entrée de l’application Flask
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

---

## ⚙️ Technologies

- **Python 3.10+**
- **Flask**
- **WTForms**
- **Jinja2**
- **JSON (fichiers)**

---

## 📌 Contraintes

- ❌ Aucune base de données relationnelle (pas de MySQL, PostgreSQL, etc.)
- ✅ Stockage via fichiers `.json`
- ✅ Respect des principes POO : héritage, polymorphisme, surcharge, constructeur
  



## 📅 Méthodologie de Travail

- **Sprints** de 2 jours
- **Stand-up meetings** quotidiens (15 min)
- Répartition flexible en cas de blocage ou retard
- Les fonctionnalités **bonus** seront traitées après le MVP

---

## ✅ Fonctionnalités Clés

-  Création / édition / suppression d’**utilisateurs**
-  Gestion de **catégories** de revenus/dépenses
-  Enregistrement de **transactions**
-  Validation de formulaires (type, champs requis, etc.)
-  Interface utilisateur HTML avec templating Jinja2
-  Persistance des données en JSON
-  Authentification sécurisée
-  Statistiques des dépenses / revenus
-  Exportation CSV des transactions
---

## 🚀 Installation et Lancement

### 1. Cloner le projet
```bash
git clone [https://github.com/votre-compte/la-pecuniaire-magique.git](https://github.com/LIKELENGE/IETC_suivi_des_depenses_personnelles.git)
cd IETC_suivi_des_depenses_personnelles
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l'application
```bash
python app.py
```



## 📁 Fichier requirements.txt

```txt
Flask==2.3.3
WTForms==3.1.2
Flask-Login==0.6.3
xhtml2pdf==0.2.11
```

---


## 📄 Licence

Projet à but pédagogique, sans licence officielle.

---
