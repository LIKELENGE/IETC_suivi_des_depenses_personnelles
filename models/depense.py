import datetime
try:
    from .transaction import Transaction
    from .classe_generique import JSONManager
except ImportError:
    from transaction import Transaction
    from classe_generique import JSONManager

chemin = "data/depenses.json"
gestionnaire = JSONManager(chemin)
#Reste à implementer la logique du système d'alerte pour les dépenses

class Depense(Transaction):
    def __init__(self, montant, date_transaction, categorie, utilisateur_id, libelle=None, id_transaction=None):
        super().__init__(montant, date_transaction, utilisateur_id, libelle)
        self.categorie = categorie

    def __str__(self):
        return f"Dépense(id={self.id_transaction}, montant={self.montant}, date={self.date_transaction}, catégorie={self.categorie}, utilisateur_id={self.utilisateur_id}, libelle={self.libelle})"

    def convert_class_vers_dict(self):
        return {
            "id_transaction": self.id_transaction,
            "montant": self.montant,
            "date_transaction": self.date_transaction,
            "categorie": self.categorie,
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
        print("Dépense modifiée.")
    
    @staticmethod
    def supprimer(id_transaction):
        def condition(item):
            return item['id_transaction'] == id_transaction
        gestionnaire.supprimer(condition)
        print("Dépense supprimée.")
    @staticmethod
    def supprimer_cascade_personne(id_personne):
        """
        Supprime toutes les dépenses associées à un utilisateur.
        """
        def condition(item):
            return item['utilisateur_id'] == id_personne
        gestionnaire.supprimer(condition)
        print("Toutes les dépenses de l'utilisateur ont été supprimées.")
    
    @staticmethod
    def supprimer_cascade_categorie(id_categorie):
        """
        Supprime toutes les dépenses associées à une catégorie.
        """
        def condition(item):
            return item['categorie'] == id_categorie
        gestionnaire.supprimer(condition)
        print("Toutes les dépenses de la catégorie ont été supprimées.")
        
    @staticmethod
    def depenses_par_utilisateur(utilisateur_id):
        """cette méthode permet de lister les dépenses par utilisateur"""
        def condition(item):
            return item['utilisateur_id'] == utilisateur_id
        depenses = gestionnaire.lire_avec_conditions(condition)
        return [Depense(**depense) for depense in depenses]
    
    @staticmethod
    def depenses_par_utilisateur_et_categorie(utilisateur_id, categorie):
        """Cette méthode permet de lister les dépenses par utilisateur et par catégorie."""
        def condition(item):
            return item['utilisateur_id'] == utilisateur_id and item['categorie'] == categorie
        depenses = gestionnaire.lire_avec_conditions(condition)
        return [Depense(**depense) for depense in depenses]
        
    
    @staticmethod
    def total_par_utilisateur_categorie_mois(utilisateur_id, categorie, mois, annee):
        """
        Calcule le total des dépenses d'un utilisateur pour une catégorie donnée,
        sur un mois et une année spécifiques.
        """
        def condition(item):
            if item['utilisateur_id'] != utilisateur_id or item['categorie'] != categorie:
                return False
            try:
                date = datetime.datetime.strptime(item['date_transaction'], "%Y-%m-%d")
                return date.month == mois and date.year == annee
            except ValueError:
                return False

        depenses = gestionnaire.lire_avec_conditions(condition)
        total = sum(float(depense['montant']) for depense in depenses)
        return total

    
    
    
    
print(Depense.total_par_utilisateur_categorie_mois("utilisateur123", "Alimentation", 11, 2023))
print(Depense.total_par_utilisateur_categorie_mois("utilisateur123", "Alimentation", 10, 2023))

    # @staticmethod
    # def depense_par_categorie_par_utilisateur(id_utilisateur, categorie):
    #     """Cette méthode permet de lister les dépenses par catégorie pour un utilisateur donné."""
    #     def condition(item):
    #         return item['categorie'] == categorie and item['utilisateur_id'] == id_utilisateur
    #     depenses = gestionnaire.lire(condition)
    #     return [Depense(**depense) for depense in depenses]



#cas d'utilisation lister les dépenses par utilisateur
#print(Depense.depenses_par_utilisateur("utilisateur123"))

#cas d'utilisation lister les dépenses par utilisateur et par catégorie
#print(Depense.depenses_par_utilisateur_et_categorie("utilisateur123", "Alimentation"))


#cas d'utilisation supprimer
#Depense.supprimer(id_transaction="b59cd0bd-e868-4b52-b240-73f9c5e0b710")
#cas d'utilisation modifier
#Depense.modifier(id_transaction="b59cd0bd-e868-4b52-b240-73f9c5e0b710",montant=50)

#cas d'utilisation ajouter
#d = Depense(100, "2023-10-01", "Alimentation", "utilisateur123", "Courses du mois")
#d.ajouter()