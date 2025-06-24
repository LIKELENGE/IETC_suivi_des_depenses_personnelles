import datetime

try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
    from .categorie_depense import CategorieDepense
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager
    from categorie_depense import CategorieDepense

chemin = "data/depenses.json"
gestionnaire_depenses = JSONManager(chemin)
chemin_categories = "data/categories_depenses.json"


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
        """Retourne une représentation textuelle lisible de l’objet Depense, utile pour l’affichage."""

        return f"Dépense(id={self.id_transaction}, montant={self.montant}, date={self.date_transaction}, heure={self.heure_transaction}, catégorie={self.categorie}, utilisateur_id={self.utilisateur_id}, libelle={self.libelle}, deductible_fiscalement={self.deductible_fiscalement})"

    def convert_class_vers_dict(self):
        """Convertit l’objet Depense en dictionnaire, nécessaire pour
        l’enregistrement dans un fichier JSON via JSONManager."""
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
        """Ajoute une dépense dans le fichier JSON en utilisant JSONManager.
        Affiche un message de confirmation après l’ajout."""
        gestionnaire_depenses.ajouter(self.convert_class_vers_dict())
        print(f" Dépense ajoutée : {self.libelle} ({self.montant}€)")

    @staticmethod
    def modifier(id_transaction, **updates):
        """Modifie une dépense existante identifiée par son ID avec les nouveaux
        attributs fournis. Affiche un message de succès après modification."""

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
        """Supprime une dépense spécifique selon son identifiant unique.
        Affiche une confirmation de suppression."""

        def condition(item):
            return item["id_transaction"] == id_transaction

        gestionnaire_depenses.supprimer(condition)
        print(f"Dépense avec l'ID {id_transaction} supprimée.")

    @staticmethod
    def supprimer_cascade_personne(utilisateur_id):
        """Supprime toutes les dépenses associées à un utilisateur donné.
        Utile lors de la suppression complète d’un utilisateur.
        """

        def condition(item):
            return item["utilisateur_id"] == utilisateur_id

        gestionnaire_depenses.supprimer(condition)
        print(
            f"Toutes les dépenses de l'utilisateur {utilisateur_id} ont été supprimées."
        )

    @staticmethod
    def supprimer_cascade_categorie(categorie_description):
        """Supprime toutes les dépenses liées à une catégorie spécifique.
        Utile lors de la suppression d’une catégorie."""

        def condition(item):
            return item["categorie"] == categorie_description

        gestionnaire_depenses.supprimer(condition)
        print(
            f"Toutes les dépenses de la catégorie '{categorie_description}' ont été supprimées."
        )

    @staticmethod
    def depenses_par_utilisateur(utilisateur_id):
        """Retourne toutes les dépenses effectuées par un utilisateur, sous forme d’objets Depense."""

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
        """Filtre les dépenses d’un utilisateur sur un mois et une année donnés.
        Très utile pour les rapports mensuels ou les analyses.
        """

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
        """Calcule la différence entre la limite fixée pour une catégorie de dépense et
            les dépenses totales déjà effectuées par l’utilisateur pour cette catégorie dans un mois donné.
        Retourne un float représentant le plafond restant. Si négatif, cela indique un dépassement.
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
