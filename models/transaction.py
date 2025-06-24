from abc import ABC, abstractmethod
from uuid import uuid4


class Transaction(ABC):
    """Cette classe représente une transaction financière. 
    Elle est abstraite et doit être étendue par des classes concrètes. 
    Elle devient soit une dépense, soit un revenu."""
    def __init__(
        self,
        utilisateur_id,
        montant: float,
        date_transaction,
        heure_transaction,
        libelle,
        id_transaction=None,
    ):
        self.id_transaction = id_transaction if id_transaction else str(uuid4()
        )
        self.utilisateur_id = utilisateur_id
        self.montant = montant
        self.libelle = libelle
        self.date_transaction = date_transaction
        self.heure_transaction = heure_transaction

    def to_dict(self):
        """Cette méthode convertit l'instance de la classe Transaction en dictionnaire."""
        return {
            "utilisateur_id": self.utilisateur_id,
            "id_transaction": self.id_transaction,
            "montant": self.montant,
            "libelle": self.libelle,
            "date_transaction": self.date_transaction,
            "heure_transaction": self.heure_transaction,
        }

    def __str__(self):
        """Cette méthode retourne une représentation en chaîne de caractères de l'instance."""
        return f"Transaction(id={self.id_transaction}, libelle='{self.libelle}', montant={self.montant}, date={self.date_transaction}, utilisateur_id={self.utilisateur_id})"

    def __repr__(self):
        """Cette méthode retourne une représentation en chaîne de caractères de l'instance."""
        return self.__str__()
