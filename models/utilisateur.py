import hashlib
from uuid import uuid4
from flask_login import UserMixin

try:
    from .classe_generique import JSONManager
    from .categorie_depense import CategorieDepense
    from .revenu import Revenu
except ImportError:
    from classe_generique import JSONManager
    from categorie_depense import CategorieDepense
    from revenu import Revenu
CHEMIN = "data/utilisateur.json"
gestionnaire = JSONManager(CHEMIN)

class Utilisateur(UserMixin):
    """Cette classe gère les utilisateurs de l'application"""
    def __init__(self, nom, prenom, email, mot_de_passe, id_utilisateur=None):
        """Cette méthode est un constructeur qui initialise un utilisateur."""
        self.id_utilisateur = id_utilisateur or str(uuid4())
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()



    def get_id(self):
        """Cette méthode retourne l'identifiant de l'utilisateur."""
        return self.id_utilisateur

    @property
    def id(self):
        """Cette méthode est utilisée par Flask-Login pour obtenir l'identifiant de l'utilisateur."""
        return self.id_utilisateur

    @staticmethod
    def get_by_id(user_id):
        """Cette méthode retourne un utilisateur à partir de son identifiant."""
        data = gestionnaire.lire()
        for item in data:
            if str(item["id_utilisateur"]) == str(user_id):
                return Utilisateur(
                    nom=item["nom"],
                    prenom=item["prenom"],
                    email=item["email"],
                    mot_de_passe=item["mot_de_passe"],
                    id_utilisateur=item["id_utilisateur"],
                )
        return None

    def convert_class_vers_dict(self):
        """Convertit l'instance de la classe Utilisateur en dictionnaire."""
        return {
            "id_utilisateur": self.id_utilisateur,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,
        }

    @staticmethod
    def verifier_email(email, id_utilisateur_actuel=None):
        """Vérifie si un email est déjà utilisé par un autre utilisateur.
        Lève une ValueError si c'est le cas."""
        utilisateurs = gestionnaire.lire()
        for u in utilisateurs:
            if u["email"] == email:
                if (
                    id_utilisateur_actuel is None
                    or u["id_utilisateur"] != id_utilisateur_actuel
                ):
                    raise ValueError(
                        "Ce mail est déjà utilisé par un autre utilisateur."
                    )

    def ajouter(self):
        """Cette méthode ajoute un nouvel utilisateur dans le fichier JSON. Verifie si l'email est unique.
        Si l'email est déjà utilisé, une ValueError est levée. 
        Sinon, l'utilisateur est ajouté et la méthode retourne 1."""
        Utilisateur.verifier_email(self.email)
        gestionnaire.ajouter(self.convert_class_vers_dict())
        return 1

    @staticmethod
    def modifier(id_utilisateur, **updates):
        """Cette méthode modifie un utilisateur dans le fichier JSON.
        Elle prend en paramètre l'identifiant de l'utilisateur et les mises à jour à effectuer."""
        nouvel_email = updates.get("email")
        if nouvel_email:
            Utilisateur.verifier_email(
                nouvel_email, id_utilisateur_actuel=id_utilisateur
            )

        def condition(item):
            return item["id_utilisateur"] == id_utilisateur

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print("Utilisateur modifié.")

    
    @staticmethod
    def supprimer(id_utilisateur):
        def condition(item):
            return item.get("id_utilisateur") == id_utilisateur

        try:
            gestionnaire.supprimer(condition)
            CategorieDepense.supprimer_cascade_personne(id_utilisateur)
            Revenu.supprimer_cascade_personne(id_utilisateur)
            print("Utilisateur supprimé.")
        except ValueError as e:
            raise ValueError("Utilisateur introuvable.") from e


    @staticmethod
    def se_connecter(email, mot_de_passe):
        """Cette méthode permet à un utilisateur de se connecter.
        Elle prend en paramètre l'email et le mot de passe de l'utilisateur. 
        Attention que le mot de passe est haché dans le fichier JSON."""
        data = gestionnaire.lire()
        mot_de_passe_hache = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        for item in data:
            if item["email"] == email and item["mot_de_passe"] == mot_de_passe_hache:
                print("Utilisateur trouvé")
                return Utilisateur(
                    nom=item["nom"],
                    prenom=item["prenom"],
                    email=item["email"],
                    mot_de_passe=item["mot_de_passe"],
                    id_utilisateur=item["id_utilisateur"],
                )
        return None


# cas d'utilisation ajouter
#u = Utilisateur("Doe", "John", "johndoe@gmail.com", "johndoe@gmail.com")
#u.ajouter()



# cas d'utilisation modifier
#Utilisateur.modifier("125f6cea-a3c2-46de-8554-78b3d4f81da6", nom ="test", prenom="test")

# cas utilisation supprimer
#Utilisateur.supprimer("test")
