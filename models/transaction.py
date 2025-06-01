from abc import ABC, abstractmethod
from uuid import uuid4
class Transaction(ABC):
    def __init__(self, montant, date_transaction, utilisateur_id, libelle = None):
        self.id_transaction = str(uuid4())
        self.montant = montant
        self.date_transaction = date_transaction
        self.utilisateur_id = utilisateur_id
        self.libelle = libelle
    
    
    def convert_class_vers_dict(self):
        return {
            "id_transaction": self.id_transaction,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "utilisateur_id": self.utilisateur_id
        }
        
    def __str__(self):
        return f"Transaction(id={self.id_transaction}, montant={self.montant}, date={self.date_transaction}, utilisateur_id={self.utilisateur_id}, libelle={self.libelle})" 
    
    #def __repr__(self):
        #return self.__str__()