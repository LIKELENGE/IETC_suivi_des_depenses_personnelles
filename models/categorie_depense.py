from uuid import uuid4

try:
    from .classe_generique import JSONManager
    
except ImportError:
    from classe_generique import JSONManager
    
CHEMIN_CATEGORIE_DEPENSE = "data/categories_depenses.json"
gestionnaire_categorie_depense = JSONManager(CHEMIN_CATEGORIE_DEPENSE)
CHEMIN_DEPENSE = "data/depenses.json"
gestionnaire_depense = JSONManager(CHEMIN_DEPENSE)


class CategorieDepense:
    """Cette classe represente categorie de dépense liées à l'utilisateur de l'application."""
    def __init__(self, description, id_utilisateur, limite, id_categorie=None):
        self.id_categorie = id_categorie or str(uuid4())
        self.description = description
        self.limite = limite
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

        if gestionnaire_categorie_depense.lire_avec_conditions(condition):
            print("Cette catégorie de dépense existe déjà pour cet utilisateur.")
            return False
        return True

    def ajouter(self):
        if self.verification_unicite(self.description, self.id_utilisateur):
            gestionnaire_categorie_depense.ajouter(self.convert_class_vers_dict())

    @staticmethod
    def modifier(id_categorie, **updates):
        if "description" in updates and "id_utilisateur" in updates:
            nouvelle_description = updates["description"]
            id_utilisateur = updates["id_utilisateur"]

            def meme_description(item):
                return (
                    item["description"] == nouvelle_description
                    and item["id_utilisateur"] == id_utilisateur
                    and item["id_categorie"] != id_categorie
                )

            deja_existe = gestionnaire_categorie_depense.lire_avec_conditions(meme_description)
            if deja_existe:
                print(
                    "Erreur : une catégorie avec cette description"
                    "existe déjà pour cet utilisateur."
                )
                return

        def condition(item):
            return item["id_categorie"] == id_categorie

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire_categorie_depense.modifier(condition, update)
        print(f"Catégorie '{id_categorie}' modifiée.")

    @staticmethod
    def afficher_categorie(id_categorie):
        """Cette méthode permet d'afficher une catégorie de dépense par son identifiant."""
        def condition(item):
            return item["id_categorie"] == id_categorie

        resultats = gestionnaire_categorie_depense.lire_avec_conditions(condition)

        if resultats:
            return CategorieDepense(**resultats[0])
        return None

    @staticmethod
    def lister_categorie_par_personne(id_utilisateur):
        """Cette méthode permet de lister les catégories de dépenses par utilisateur."""
        def condition(item):
            return item["id_utilisateur"] == id_utilisateur

        categories_depenses = gestionnaire_categorie_depense.lire_avec_conditions(condition)
        return [
            CategorieDepense(**categorie_depense)
            for categorie_depense in categories_depenses
        ]
    @staticmethod
    def supprimer(id_categorie):
        def condition_categorie(item):
            print("Vérification catégorie :", item.get("id_categorie"))
            return item.get("id_categorie") == id_categorie

        if not gestionnaire_categorie_depense.supprimer(condition_categorie):
            raise ValueError(f"Catégorie '{id_categorie}' introuvable.")

        def condition_depense(item):
            print("Vérification dépense :", item.get("categorie"))
            return item.get("categorie") == id_categorie

        gestionnaire_depense.supprimer(condition_depense)
        print(f"Catégorie '{id_categorie}' et ses dépenses associées ont été supprimées.")



    @staticmethod
    def supprimer_cascade_personne(id_personne):
        """Supprime toutes les catégories de dépense associées à un utilisateur"""

        def condition(item):
            return item["id_utilisateur"] == id_personne

        gestionnaire_categorie_depense.supprimer(condition)

    @staticmethod
    def afficher_categorie_par_utilisateur(id_utilisateur):
        """Cette méthode permet d'afficher les catégories de dépenses par utilisateur."""
        def condition(item):
            return item["id_utilisateur"] == id_utilisateur

        categories = gestionnaire_categorie_depense.lire_avec_conditions(condition)
        return [CategorieDepense(**categorie) for categorie in categories]

    @staticmethod
    def afficher_limite(id_categorie):
        """Cette méthode permet d'afficher la limite d'une catégorie de dépense par son identifiant."""
        def condition(item):
            return item["id_categorie"] == id_categorie

        limite = gestionnaire_categorie_depense.lire_avec_conditions(condition)
        return limite[0]["limite"]


# cas d'utilisation ajouter
# c = CategorieDepense("loyer", 500, "utilisateur123", )
# c.ajouter()

# CategorieDepense.modifier(
#     id_categorie="9c180bde-3aa1-4c2d-9e12-f43b4fc7e847",
#     description="Loyer principal",
#     limite=700,
#     id_utilisateur="utilisateur123"
# )


CategorieDepense.supprimer("1")