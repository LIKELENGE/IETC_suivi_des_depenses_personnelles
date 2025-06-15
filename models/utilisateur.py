import hashlib
from uuid import uuid4
from flask_login import UserMixin


try:
    from .classe_generique import JSONManager
except ImportError:
    from classe_generique import JSONManager

chemin = "data/utilisateur.json"
gestionnaire = JSONManager(chemin)


class Utilisateur(UserMixin):
    """Cette classe gère les utilisateurs de l'application"""

    def __init__(self, nom, prenom, email, mot_de_passe, id_utilisateur=None):
        self.id_utilisateur = id_utilisateur or str(uuid4())
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()

    @staticmethod
    def from_dict(data):
        """Crée une instance d'Utilisateur à partir d'un dictionnaire."""
        utilisateur = Utilisateur(
            email=data["email"], nom=data["nom"], prenom=data["prenom"], mot_de_passe=""
        )
        utilisateur.id_utilisateur = data["id_utilisateur"]
        utilisateur.mot_de_passe = data["mot_de_passe"]

    def get_id(self):
        return self.id_utilisateur
    
    @property
    def id(self):
        return self.id_utilisateur
    
    @staticmethod
    def get_by_id(user_id):
        data = gestionnaire.lire()
        for item in data:
            if str(item["id_utilisateur"]) == str(user_id):
                return Utilisateur(
                    nom=item["nom"],
                    prenom=item["prenom"],
                    email=item["email"],
                    mot_de_passe=item["mot_de_passe"],
                    id_utilisateur=item["id_utilisateur"]
                )
        return None

    
    def convert_class_vers_dict(self):
        return {
            "id_utilisateur": self.id_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe
        }
    
    @staticmethod
    def verifier_email(email, id_utilisateur_actuel=None):
        """Vérifie si un email est déjà utilisé par un autre utilisateur.
        Lève une ValueError si c'est le cas."""
        utilisateurs = gestionnaire.lire()
        for u in utilisateurs:
            if u["email"] == email:
                if id_utilisateur_actuel is None or u["id_utilisateur"] != id_utilisateur_actuel:
                    raise ValueError("Ce mail est déjà utilisé par un autre utilisateur.")
                
    def ajouter(self):
        Utilisateur.verifier_email(self.email)  # lèvera une erreur si nécessaire
        gestionnaire.ajouter(self.convert_class_vers_dict())
        return 1

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

    
    @staticmethod
    def se_connecter(email, mot_de_passe):
        data = gestionnaire.lire()
        mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        for item in data:
            if item["email"] == email and item["mot_de_passe"] == mot_de_passe_hache:
                print("Utilisateur trouvé")
                return Utilisateur(nom=item["nom"], prenom=item["prenom"],email=item["email"], mot_de_passe=item["mot_de_passe"], id_utilisateur=item["id_utilisateur"])
        return None
        

#cas d'utilisation ajouter
#u = Utilisateur("Dupont", "Jean", "test@gmail.com", "test@gmail.com")
#u.ajouter()

#cas d'utilisation modifier
#Utilisateur.modifier("125f6cea-a3c2-46de-8554-78b3d4f81da6", nom ="test", prenom="test")

#cas utilisation supprimer
#Utilisateur.supprimer("125f6cea-a3c2-46de-8554-78b3d4f81da6")