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

    def to_dict(self):
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
        # Empêche les doublons de description
        data = gestionnaire.lire()
        if any(item["description"] == self.description for item in data):
            print(f"Erreur : La description '{self.description}' existe déjà.")
            return False
        gestionnaire.ajouter(self.to_dict())
        print(f"✅ Catégorie '{self.description}' ajoutée.")
        return True

    def modifier(self, nouvelle_description=None, nouvelle_limite=None):
        def condition(item):
            return item["id_categorie"] == self.id_categorie

        def update(item):
            if nouvelle_description:
                item["description"] = nouvelle_description
            if nouvelle_limite is not None:
                item["limite"] = nouvelle_limite

        gestionnaire.modifier(condition, update)
        print(f"✏️ Catégorie '{self.id_categorie}' modifiée.")

    def supprimer(self):
        gestionnaire.supprimer(lambda item: item["id_categorie"] == self.id_categorie)
        print(f"🗑️ Catégorie '{self.id_categorie}' supprimée.")

    @staticmethod
    def afficher_toutes():
        data = gestionnaire.lire()
        if not data:
            print("Aucune catégorie enregistrée.")
        else:
            print("📋 Liste des catégories :")
            for item in data:
                print(f"- [{item['id_categorie']}] {item['description']} (limite: {item['limite']}€, utilisateur: {item['id_utilisateur']})")