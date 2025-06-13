"""
Fichier categorie_depense

Ce fichier contient la classe CategorieDepense qui permet de gérer les catégories de dépenses
d’un utilisateur dans un système de gestion des depenses personnel.

Les données sont stockées dans un fichier JSON via un gestionnaire générique.
"""
from uuid import uuid4
try:
    from .classe_generique import JSONManager
except ImportError:
    from classe_generique import JSONManager

CHEMIN = "data/categories_depenses.json"
gestionnaire = JSONManager(CHEMIN)


class CategorieDepense:
    """ Cette classe represente categorie de dépense liées à l'utilisateur de l'application
    Avec
    lES attributs;
        id_categorie (str) : Identifiant unique de la catégorie (UUID).
        description (str) : Nom ou description de la catégorie (ex : 'loyer', 'courses').
        limite (float/int) : Montant limite autorisé pour cette catégorie.
        id_utilisateur (str) : Identifiant de l’utilisateur auquel appartient la catégorie.
    Les méthodes:
        ajouter() : Ajoute la catégorie dans le fichier JSON si elle est unique.
        modifier() : Modifie les propriétés d’une catégorie existante.
        supprimer() : Supprime une catégorie existante.
        lister_categorie_par_personne() : Lister les catégories liées à un utilisateur.
        afficher_categorie() : Afficher une catégorie spécifique par son ID.
    """
    def __init__(self, description, id_utilisateur, limite,id_categorie=None):
        self.id_categorie = id_categorie or str(uuid4())
        self.description = description
        self.limite =  limite
        self.id_utilisateur = id_utilisateur
        
    def convert_class_vers_dict(self):
        return {
            "id_categorie": self.id_categorie,
            "description": self.description,
            "limite": self.limite,
            "id_utilisateur": self.id_utilisateur,
            
        }
    @staticmethod
    def verification_unicite(description, id_utilisateur):
        def condition(item):
            return (
                item["description"] == description 
                and item["id_utilisateur"] == id_utilisateur
            )
        if gestionnaire.lire_avec_conditions(condition):
            print("Cette catégorie de dépense existe déjà pour cet utilisateur.")
            return False
        return True
 
    def ajouter(self):
        if self.verification_unicite(self.description, self.id_utilisateur):
            gestionnaire.ajouter(self.convert_class_vers_dict())

  
    @staticmethod
    def modifier(id_categorie, **updates):
        if "description" in updates and "id_utilisateur" in updates:
            nouvelle_description = updates["description"]
            id_utilisateur = updates["id_utilisateur"]

            def meme_description(item):
                return (
                    item["description"] == nouvelle_description and
                    item["id_utilisateur"] == id_utilisateur and
                    item["id_categorie"] != id_categorie 
                )

            deja_existe = gestionnaire.lire_avec_conditions(meme_description)
            if deja_existe:
                print("Erreur : une catégorie avec cette description"
                       "existe déjà pour cet utilisateur."
                     )
                return

        def condition(item):
            return item["id_categorie"] == id_categorie

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print(f"Catégorie '{id_categorie}' modifiée.")

    @staticmethod
    def afficher_categorie(id_categorie):
        def condition(item):
            return item["id_categorie"] == id_categorie

        resultats = gestionnaire.lire_avec_conditions(condition)
        
        if resultats:
            return CategorieDepense(**resultats[0]) 
        return None

    @staticmethod
    def lister_categorie_par_personne(id_utilisateur):
        def condition(item):
            return item["id_utilisateur"] == id_utilisateur
        categories_depenses = gestionnaire.lire_avec_conditions(condition)
        return [CategorieDepense(**categorie_depense) for categorie_depense in categories_depenses]

    @staticmethod
    def supprimer(id_categorie):
        def condition(item):
            return item["id_categorie"] == id_categorie

        gestionnaire.supprimer(condition)


#cas d'utilisation ajouter
#c = CategorieDepense("loyer", 500, "utilisateur123", )
#c.ajouter()

# CategorieDepense.modifier(
#     id_categorie="9c180bde-3aa1-4c2d-9e12-f43b4fc7e847",
#     description="Loyer principal",
#     limite=700,
#     id_utilisateur="utilisateur123"  
# )
