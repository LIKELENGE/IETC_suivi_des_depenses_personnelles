from datetime import datetime
from uuid import uuid4

try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager

CHEMIN = "data/revenus.json"
gestionnaire = JSONManager(CHEMIN)

class Revenu(Transaction):
    """Cette classe gère les revenus des utilisateurs de l'application. Elle hérite de la classe Transaction."""
    


    def __init__(
              
        self,
        utilisateur_id,
        montant,
        date_transaction,
        heure_transaction,
        libelle="",
        id_transaction=None,
        imposable=True,
    ):
        super().__init__(
            """Initialise une instance de la classe Revenu, héritée de Transaction, 
            avec des attributs comme le montant, la date/heure, le libellé, 
            et un indicateur d’imposabilité."""

            utilisateur_id,
            montant,
            date_transaction,
            heure_transaction,
            libelle,
            id_transaction,
        )
        self.imposable = imposable

    def convert_class_vers_dict(self):
        """ Convertit une instance de Revenu en dictionnaire.
Cette méthode est une surcharge de celle définie dans la classe Transaction.
"""
        
        return {
            "id_transaction": self.id_transaction,
            "utilisateur_id": self.utilisateur_id,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "heure_transaction": self.heure_transaction,
            "imposable": self.imposable,
            "libelle": self.libelle,
        }

    def ajouter(self):
        """Ajoute un revenu à la base de données (fichier JSON), en appelant le gestionnaire JSONManager.
"""
        
        gestionnaire.ajouter(self.convert_class_vers_dict())

    @staticmethod
    def modifier(id_transaction, **updates):
        """Modifie un revenu existant identifié par son id_transaction, en mettant à jour les champs spécifiés.
Affiche un message de confirmation après modification."""
        def condition(item):
            return item["id_transaction"] == id_transaction

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print("Revenu modifié.")

    @staticmethod
    def supprimer(id_transaction):
        """Supprime un revenu spécifique à partir de son identifiant.
Affiche un message de confirmation après suppression."""
       
        def condition(item):
            return item["id_transaction"] == id_transaction

        gestionnaire.supprimer(condition)
        print("Revenu supprimé.")

    @staticmethod
    def revenue_par_utilisateur(utilisateur_id):
        """ Récupère tous les revenus enregistrés pour un utilisateur donné.
Retourne une liste d’objets Revenu.
"""
        
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        revenus = gestionnaire.lire_avec_conditions(condition)
        return [Revenu(**revenu) for revenu in revenus]

    @staticmethod
    def revenus_par_utilisateur_et_mois(utilisateur_id, mois, annee):
        """ Filtre les revenus d’un utilisateur pour un mois et une année donnés.
Retourne une liste de revenus correspondant à la période spécifiée."""
        
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        revenus = gestionnaire.lire_avec_conditions(condition)

        revenus_filtrés = []

        for revenu in revenus:
            date_revenu = datetime.strptime(revenu["date_transaction"], "%Y-%m-%d")
            if date_revenu.year == annee and date_revenu.month == mois:
                revenus_filtrés.append(Revenu(**revenu))

        return revenus_filtrés
    
    def supprimer_cascade_personne(utilisateur_id):
        """Supprime tous les revenus associés à un utilisateur donné.
Utilisé notamment lors de la suppression complète d’un utilisateur de la plateforme."""
        
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        gestionnaire.supprimer(condition)
        print(f"Tous les revenus de l'utilisateur {utilisateur_id} ont été supprimés.")


# cas d'utilisation ajouter
# r = Revenu(1000, "2023-10-01", "utilisateur123", imposable=True, libelle="retour impot")
# r.ajouter()
# cas d'utilisation modifier
# Revenu.modifier("05b26529-6387-41fa-8daf-e0a143f3a1f7", montant=1200, libelle="prime de fin d'année")
# cas d'utilisation supprimer
# Revenu.supprimer("05b26529-6387-41fa-8daf-e0a143f3a1f7")
