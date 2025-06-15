"""
Fichier revenu

Ce fichier contient la classe Revenu, qui hérite de la classe Transaction.

Elle permet de gérer les revenus d’un utilisateur dans une application de gestion financière.
Les revenus sont stockés dans un fichier JSON via un gestionnaire générique.
"""
try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager

chemin = "data/revenus.json"   
gestionnaire = JSONManager(chemin)
class Revenu(Transaction):
    """
    Cette classe représente un revenu enregistré par un utilisateur.

    Attributs :
        id_transaction (str) : Identifiant unique hérité de la classe Transaction.
        montant (float/int) : Montant du revenu.
        date_transaction (str) : Date à laquelle le revenu a été enregistré.
        utilisateur_id (str) : Identifiant de l’utilisateur concerné.
        libelle (str) : Description facultative du revenu.
        imposable (bool) : Indique si le revenu est imposable (par défaut : True).

    Méthodes :
        convert_class_vers_dict() : Convertit l'objet en dictionnaire pour le stockage JSON.
        ajouter() : Ajoute un revenu au fichier s’il est valide.
        modifier(id_transaction, **updates) : Modifie un revenu existant selon l’ID.
        supprimer(id_transaction) : Supprime un revenu par son ID.
        revenue_par_utilisateur(utilisateur_id) : Liste les revenus liés à un utilisateur donné.
    """
    def __init__(self, montant, date_transaction, utilisateur_id, imposable=True, libelle=None):
        super().__init__(montant, date_transaction, utilisateur_id, libelle)
        self.imposable = imposable

    def convert_class_vers_dict(self):
        return {
            "id_transaction": self.id_transaction,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "imposable": self.imposable,
            "utilisateur_id": self.utilisateur_id,
            "libelle": self.libelle
        }

    def ajouter(self):
        gestionnaire.ajouter(self.convert_class_vers_dict())

    @staticmethod
    def modifier(id_transaction, **updates):
        def condition(item):
            return item['id_transaction'] == id_transaction

        def update(item):
            for key, value in updates.items():
                if key in item:
                    item[key] = value

        gestionnaire.modifier(condition, update)
        print("Revenu modifié.")

    @staticmethod
    def supprimer(id_transaction):
        def condition(item):
            return item['id_transaction'] == id_transaction
        gestionnaire.supprimer(condition)
        print("Revenu supprimé.")
    
    def revenue_par_utilisateur(utilisateur_id):
        def condition(item):
            return item['utilisateur_id'] == utilisateur_id
        revenus = gestionnaire.lister(condition)
        return [Revenu(**revenu) for revenu in revenus]
    
#cas d'utilisation ajouter
#r = Revenu(1000, "2023-10-01", "utilisateur123", imposable=True, libelle="retour impot")
#r.ajouter()
#cas d'utilisation modifier
#Revenu.modifier("05b26529-6387-41fa-8daf-e0a143f3a1f7", montant=1200, libelle="prime de fin d'année")
#cas d'utilisation supprimer
#Revenu.supprimer("05b26529-6387-41fa-8daf-e0a143f3a1f7")