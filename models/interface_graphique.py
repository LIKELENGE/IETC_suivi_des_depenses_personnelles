import tkinter as tk
from tkinter import messagebox
from models.categorie_depense import CategorieDepense


def ajouter_categorie():
    description = entry_description.get()
    try:
        limite = float(entry_limite.get())
    except ValueError:
        messagebox.showerror("Erreur", "Limite invalide.")
        return

    id_utilisateur = entry_utilisateur.get()
    cat = CategorieDepense(description, limite, id_utilisateur)
    if cat.ajouter():
        messagebox.showinfo("Succès", "Catégorie ajoutée.")
        afficher_toutes()


def afficher_toutes():
    text_resultat.delete("1.0", tk.END)
    data = CategorieDepense.afficher_toutes()
    if data:
        for item in data:
            ligne = f"[{item['id_categorie']}] {item['description']} - {item['limite']}€ - {item['id_utilisateur']}\n"
            text_resultat.insert(tk.END, ligne)


# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestion des Catégories de Dépenses")

# Champs d'entrée
tk.Label(fenetre, text="Description").grid(row=0, column=0)
entry_description = tk.Entry(fenetre)
entry_description.grid(row=0, column=1)

tk.Label(fenetre, text="Limite (€)").grid(row=1, column=0)
entry_limite = tk.Entry(fenetre)
entry_limite.grid(row=1, column=1)

tk.Label(fenetre, text="ID Utilisateur").grid(row=2, column=0)
entry_utilisateur = tk.Entry(fenetre)
entry_utilisateur.grid(row=2, column=1)

# Boutons
btn_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter_categorie)
btn_ajouter.grid(row=3, column=0, columnspan=2, pady=10)

# Zone d'affichage des résultats
text_resultat = tk.Text(fenetre, height=10, width=60)
text_resultat.grid(row=4, column=0, columnspan=2)

# Afficher les catégories au démarrage
afficher_toutes()

# Lancement de l'interface
fenetre.mainloop()
