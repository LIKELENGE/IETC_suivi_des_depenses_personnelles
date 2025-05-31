from uuid import uuid4
from .classe_generique import JSONManager

chemin = "data/categories.json"
gestionnaire = JSONManager(chemin)


class CategorieDepense:
    def __init__(self, description, limite, id_utilisateur, id_categorie=None):
        self.id_categorie = id_categorie or str(uuid4())
        self.description = description
        self.limite = limite
        self.id_utilisateur = id_utilisateur

    def convert_class_vers_dict(self):
        return {
            "id_categorie": self.id_categorie,
            "description": self.description,
            "limite": self.limite,
            "id_utilisateur": self.id_utilisateur
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_categorie=data.get("id_categorie"),
            description=data.get("description"),
            limite=data.get("limite"),
            id_utilisateur=data.get("id_utilisateur")
        )

    def ajouter(self):
      #il faut ajouter la logique la vrfication du doublon
      gestionnaire.ajouter(self.convert_class_vers_dict())

    @staticmethod
    def modifier(id_categorie, **updates):
        def condition(item):
            return item["id_categorie"] == id_categorie

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value


        gestionnaire.modifier(condition, update)
        print(f"Catégorie '{id_categorie}' modifiée.")

    @staticmethod
    def supprimer(id_categorie):
        def condition(item):
            return item['id_categorie'] == id_categorie
        gestionnaire.supprimer(condition)       
        print("categorie de dépense")


    @staticmethod
    def lister_categorie_par_personne():
        data = gestionnaire.lire()
        if not data:
            print("Aucune catégorie enregistrée.")
        else:
            print("Liste des catégories par utilisateur :")
            categories_par_utilisateur = {}
            for item in data:
                utilisateur = item['id_utilisateur']
                if utilisateur not in categories_par_utilisateur:
                    categories_par_utilisateur[utilisateur] = []
                categories_par_utilisateur[utilisateur].append(item)
            for utilisateur, categories in categories_par_utilisateur.items():
                print(f"\nUtilisateur : {utilisateur}")
                for cat in categories:
                    print(f"- [{cat['id_categorie']}] {cat['description']} (limite: {cat['limite']}€)")
