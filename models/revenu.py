from datetime import datetime
from uuid import uuid4


try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager


chemin = "data/revenus.json"
gestionnaire = JSONManager(chemin)


class Revenu(Transaction):
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
            utilisateur_id,
            montant,
            date_transaction,
            heure_transaction,
            libelle,
            id_transaction,
        )
        self.imposable = imposable

    def convert_class_vers_dict(self):
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
        gestionnaire.ajouter(self.convert_class_vers_dict())

    @staticmethod
    def modifier(id_transaction, **updates):
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
        def condition(item):
            return item["id_transaction"] == id_transaction

        gestionnaire.supprimer(condition)
        print("Revenu supprimé.")

    @staticmethod
    def revenue_par_utilisateur(utilisateur_id):
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        revenus = gestionnaire.lire_avec_conditions(condition)
        return [Revenu(**revenu) for revenu in revenus]

    @staticmethod
    def revenus_par_utilisateur_et_mois(utilisateur_id, mois, annee):
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        revenus = gestionnaire.lire_avec_conditions(condition)

        revenus_filtrés = []

        for revenu in revenus:
            date_revenu = datetime.strptime(revenu["date_transaction"], "%Y-%m-%d")
            if date_revenu.year == annee and date_revenu.month == mois:
                revenus_filtrés.append(Revenu(**revenu))

        return revenus_filtrés


# cas d'utilisation ajouter
# r = Revenu(1000, "2023-10-01", "utilisateur123", imposable=True, libelle="retour impot")
# r.ajouter()
# cas d'utilisation modifier
# Revenu.modifier("05b26529-6387-41fa-8daf-e0a143f3a1f7", montant=1200, libelle="prime de fin d'année")
# cas d'utilisation supprimer
# Revenu.supprimer("05b26529-6387-41fa-8daf-e0a143f3a1f7")
