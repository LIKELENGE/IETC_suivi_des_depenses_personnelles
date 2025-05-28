import json
import os

#encoding: utf-8 pour avoir les accents correctement gérés dans les fichiers JSON
class JSONManager:
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

    def modifier(self, condition_fn, update_fn):
        data = self.lire()
        for item in data:
            if condition_fn(item):
                update_fn(item)
        self.ecrire(data)
