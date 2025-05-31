try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager

chemin = "data/depenses.json"
gestionnaire = JSONManager(chemin)
#Reste à implementer la logique du système d'alerte pour les dépenses

class Depense(Transaction):
    def __init__(self, montant, date_transaction, categorie, utilisateur_id, libelle=None):
        super().__init__(montant, date_transaction, utilisateur_id, libelle)
        self.categorie = categorie

    def convert_class_vers_dict(self):
        return {
            "id_transaction": self.id_transaction,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "categorie": self.categorie,
            "personne_id": self.utilisateur_id,
            "libelle": self.libelle
        }
    
    def ajouter(self):
        gestionnaire.ajouter(self.convert_class_vers_dict())
    
    def modifer(self, condition_fn, update_fn):
        gestionnaire.modifier(condition_fn, update_fn)
    
    @staticmethod
    def modifier(id_transaction, **updates):
        def condition(item):
            return item['id_transaction'] == id_transaction

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print("Dépense modifiée.")
    
    @staticmethod
    def supprimer(id_transaction):
        def condition(item):
            return item['id_transaction'] == id_transaction
        gestionnaire.supprimer(condition)
        print("Dépense supprimée.")


#cas d'utilisation supprimer
#Depense.supprimer(id_transaction="b59cd0bd-e868-4b52-b240-73f9c5e0b710")
#cas d'utilisation modifier
#Depense.modifier(id_transaction="b59cd0bd-e868-4b52-b240-73f9c5e0b710",montant=250)

#cas d'utilisation ajouter
#d = Depense(100, "2023-10-01", "Alimentation", "utilisateur123", "Courses du mois")
#d.ajouter()