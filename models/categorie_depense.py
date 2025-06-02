from uuid import uuid4
try:
    from .classe_generique import JSONManager
except ImportError:
    from classe_generique import JSONManager

chemin = "data/categories_depenses.json"
gestionnaire = JSONManager(chemin)


class CategorieDepense:
    """_les contraintes de la classe CategorieDepense sont les suivantes: _
        type_periode peut être "mensuel", "hebdomadaire", "annuel" "trimestriel", 
        "quadrimestriel " ou "semestriel" cette contrainte sera gérée au niveau du validateur (form) 
        pour n'est pas trop charger la logique de la classe
        la modification de la periode doit être interdite une fois la catégorie créée
        la modification dois se faire en respectant la logique de la catégorie
        avant d'enregistrer la modifition de la période, il faut vérifier si la limite est respectée
        
    """
    def __init__(self, description, limite, id_utilisateur, type_periode = "mensuelle", id_categorie=None):
        self.id_categorie = id_categorie or str(uuid4())
        self.description = description
        self.limite = limite
        self.id_utilisateur = id_utilisateur
        self.type_periode = type_periode



    def convert_class_vers_dict(self):
        return {
            "id_categorie": self.id_categorie,
            "description": self.description,
            "limite": self.limite,
            "id_utilisateur": self.id_utilisateur,
            "type_periode": self.type_periode
        }


    @staticmethod
    def verification_unicite(description, id_utilisateur):
        def condition(item):
            return item["description"] == description and item["id_utilisateur"] == id_utilisateur
        if gestionnaire.lire_avec_conditions(condition):
            print("Cette catégorie de dépense existe déjà pour cet utilisateur.")
            return False
        return True
    
    def ajouter(self):
        if self.verification_unicite(self.description, self.id_utilisateur):
            gestionnaire.ajouter(self.convert_class_vers_dict())

    
    @staticmethod
    def modifier(id_categorie, **updates):
        # Interdiction de modifier la période
        if "type_periode" in updates:
            print("La modification du champ 'type_periode' est interdite.")
            return

        # Vérifier unicité si description est modifiée
        if "description" in updates and "id_utilisateur" in updates:
            nouvelle_description = updates["description"]
            id_utilisateur = updates["id_utilisateur"]

            def meme_description(item):
                return (
                    item["description"] == nouvelle_description and
                    item["id_utilisateur"] == id_utilisateur and
                    item["id_categorie"] != id_categorie  # Ne pas comparer avec elle-même
                )

            deja_existe = gestionnaire.lire_avec_conditions(meme_description)
            if deja_existe:
                print("Erreur : une catégorie avec cette description existe déjà pour cet utilisateur.")
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
    def lister_categorie_par_personne(utilisateur_id):
        """cette méthode permet de lister les catégories de dépenses par utilisateur"""
        def condition(item):
            return item['utilisateur_id'] == utilisateur_id
        categories = gestionnaire.lister(['utilisateur_id'] == utilisateur_id)
        return [categorie(**categorie) for categorie in categories]


#cas d'utilisation ajouter
#c = CategorieDepense("loyer", 500, "utilisateur123", type_periode="mensuelle")
#c.ajouter()

# CategorieDepense.modifier(
#     id_categorie="9c180bde-3aa1-4c2d-9e12-f43b4fc7e847",
#     description="Loyer principal",
#     limite=700,
#     id_utilisateur="utilisateur123"  # Nécessaire pour vérifier unicité
# )
