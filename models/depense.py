import datetime

try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
    from .categorie_depense import CategorieDepense
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager
    from categorie_depense import CategorieDepense

chemin_depenses = "data/depenses.json"
gestionnaire_depenses = JSONManager(chemin_depenses)
chemin_categories = "data/categories_depenses.json"
gestionnaire_categories = JSONManager(chemin_categories)


class Depense(Transaction):
    """Cette classe gère les dépenses des utilisateurs de l'application. Elle hérite de la classe Transaction."""
    def __init__(
        self,
        utilisateur_id,
        montant,
        date_transaction,
        heure_transaction,
        categorie,
        libelle="",
        id_transaction=None,
        deductible_fiscalement=True,
    ):
        super().__init__(
            utilisateur_id,
            float(montant),
            date_transaction,
            heure_transaction,
            libelle,
            id_transaction,
        )
        self.categorie = categorie
        self.deductible_fiscalement = deductible_fiscalement

    def __str__(self):
        
        return f"Dépense(id={self.id_transaction}, montant={self.montant}, date={self.date_transaction}, heure={self.heure_transaction}, catégorie={self.categorie}, utilisateur_id={self.utilisateur_id}, libelle={self.libelle}, deductible_fiscalement={self.deductible_fiscalement})"

    def convert_class_vers_dict(self):
        return {
            "id_transaction": self.id_transaction,
            "utilisateur_id": self.utilisateur_id,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "heure_transaction": self.heure_transaction,
            "categorie": self.categorie,
            "libelle": self.libelle,
            "deductible_fiscalement": self.deductible_fiscalement,
        }

    def ajouter(self):
        """Cette méthode ajoute une dépense à la liste des dépenses de l'utilisateur."""
        gestionnaire_depenses.ajouter(self.convert_class_vers_dict())
        print(f" Dépense ajoutée : {self.libelle} ({self.montant}€)")

    @staticmethod
    def modifier(id_transaction, **updates):
        def condition(item):
            return item["id_transaction"] == id_transaction

        def update_func(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value
            return item

        gestionnaire_depenses.modifier(condition, update_func)
        print(f"Dépense avec l'ID {id_transaction} modifiée.")

    @staticmethod
    def supprimer(id_transaction):
        def condition(item):
            return item["id_transaction"] == id_transaction

        gestionnaire_depenses.supprimer(condition)
        print(f"Dépense avec l'ID {id_transaction} supprimée.")

    @staticmethod
    def supprimer_cascade_personne(utilisateur_id):
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        gestionnaire_depenses.supprimer(condition)
        print(
            f"Toutes les dépenses de l'utilisateur {utilisateur_id} ont été supprimées."
        )

    @staticmethod
    def supprimer_cascade_categorie(categorie_description):
        def condition(item):
            return item["categorie"] == categorie_description

        gestionnaire_depenses.supprimer(condition)
        print(
            f"Toutes les dépenses de la catégorie '{categorie_description}' ont été supprimées."
        )

    @staticmethod
    def depenses_par_utilisateur(utilisateur_id):
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        depenses_data = gestionnaire_depenses.lire_avec_conditions(condition)
        return [
            Depense(
                montant=d["montant"],
                date_transaction=d["date_transaction"],
                heure_transaction=d["heure_transaction"],
                categorie=d["categorie"],
                utilisateur_id=d["utilisateur_id"],
                libelle=d["libelle"],
                id_transaction=d["id_transaction"],
                deductible_fiscalement=d["deductible_fiscalement"],
            )
            for d in depenses_data
        ]

    @staticmethod
    def depenses_par_utilisateur_et_mois(utilisateur_id, mois, annee):
        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        depenses = gestionnaire_depenses.lire_avec_conditions(condition)
        depenses_filtrées = []

        for depense in depenses:
            date_depense = datetime.datetime.strptime(
                depense["date_transaction"], "%Y-%m-%d"
            )
            if date_depense.year == annee and date_depense.month == mois:
                depenses_filtrées.append(Depense(**depense))

        return depenses_filtrées

    @staticmethod
    def verifier_limite(utilisateur_id, mois, annee, id_categorie):
        """
        Calcule le montant restant que l'utilisateur peut dépenser pour une catégorie donnée,
        au cours d’un mois et d’une année spécifiques, sans dépasser la limite fixée.

        Retourne un float représentant la différence entre la limite de la catégorie et
        le total des dépenses déjà enregistrées pour cette catégorie sur la période.
        Si le résultat est négatif, cela indique un dépassement de la limite.
        """
        depenses = Depense.depenses_par_utilisateur_et_mois(utilisateur_id, mois, annee)
        depenses_filtre_categorie = [
            depense for depense in depenses if depense.categorie == id_categorie
        ]
        total_depense = sum(depense.montant for depense in depenses_filtre_categorie)
        limite_cateorie = CategorieDepense.afficher_limite(id_categorie)
        plafond_restant_categorie = limite_cateorie - total_depense
        return plafond_restant_categorie




# d = Depense("818b873d-c6f2-47a1-8995-41da0623f0c8", 150, "2025-06-15", "14:28", "e147918c-fdbf-4606-806f-39ea52800e1c", "test")
# d.ajouter()
