import hashlib
from uuid import uuid4


try:
    from .classe_generique import JSONManager
except ImportError:
    from classe_generique import JSONManager

chemin = "data/utilisateur.json"
gestionnaire = JSONManager(chemin)

class Utilisateur:
    def __init__(self, nom, prenom, email, mot_de_passe, id_utilisateur=None):
        self.id_utilisateur = id_utilisateur or str(uuid4())
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    
    def convert_class_vers_dict(self):
        return {
            "id_utilisateur": self.id_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe
        }
    
    def ajouter(self):
        gestionnaire.ajouter(self.convert_class_vers_dict())
    
    @staticmethod
    def modifier(id_utilisateur, **updates):
        def condition(item):
            return item['id_utilisateur'] == id_utilisateur

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print("Utilisateur modifié.")
    
    @staticmethod
    def supprimer(id_utilisateur):
        def condition(item):
            return item['id_utilisateur'] == id_utilisateur
        gestionnaire.supprimer(condition)
        print("Utilisateur supprimé.")
        

#cas d'utilisation ajouter
#u = Utilisateur("Dupont", "Jean", "jeandupont@gmail.com", "jeandupont@gmail.com")
#u.ajouter()

#cas d'utilisation modifier
#Utilisateur.modifier("125f6cea-a3c2-46de-8554-78b3d4f81da6", nom ="test", prenom="test")

#cas utilisation supprimer
#Utilisateur.supprimer("125f6cea-a3c2-46de-8554-78b3d4f81da6")