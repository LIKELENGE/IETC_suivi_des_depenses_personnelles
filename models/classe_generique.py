import json
import os

#encoding: utf-8 pour avoir les accents correctement gérés dans les fichiers JSON
class JSONManager:
    """
    Cette classe sert de gestionnaire générique pour la manipulation de fichiers JSON.
    
    Elle permet de centraliser toutes les opérations liées à la persistance des données 
    (lecture, écriture, ajout, suppression, mise à jour, filtrage).

    Attributs :
        chemin (str) : Chemin du fichier JSON à manipuler.

    Méthodes :
        lire() : Lit les données du fichier JSON et retourne une liste d'objets.
        ecrire(data) : Écrit la liste d'objets fournie dans le fichier JSON.
        ajouter(objet_dict) : Ajoute un nouvel objet à la liste JSON.
        supprimer(condition_fn) : Supprime les objets qui remplissent la condition donnée.
        modifier(condition_fn, update_fn) : Modifie les objets qui remplissent la condition.
        lire_avec_conditions(*conditions) : Retourne les objets qui remplissent toutes les conditions fournies.
    """
    def __init__(self, chemin_fichier):
        self.chemin = chemin_fichier
        os.makedirs(os.path.dirname(self.chemin), exist_ok=True)

    def lire(self):
        if os.path.exists(self.chemin):
            with open(self.chemin, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def ecrire(self, data):
        with open(self.chemin, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def ajouter(self, objet_dict):
        data = self.lire()
        data.append(objet_dict)
        self.ecrire(data)

    def supprimer(self, condition_fn):
        data = self.lire()
        data_filtrée = [item for item in data if not condition_fn(item)]
        self.ecrire(data_filtrée)
        return len(data_filtrée) < len(data)


    def modifier(self, condition_fn, update_fn):
        data = self.lire()
        for item in data:
            if condition_fn(item):
                update_fn(item)
        self.ecrire(data)
        
    def lire_avec_conditions(self, *conditions):
        data = self.lire()
        for cond in conditions:
            data = [item for item in data if cond(item)]
        return data

