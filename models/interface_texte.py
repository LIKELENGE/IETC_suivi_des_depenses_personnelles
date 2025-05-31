from models.categorie_depense import CategorieDepense


def afficher_menu():
    print("\n=== MENU GESTION DES CATÉGORIES ===")
    print("1. Ajouter une catégorie")
    print("2. Modifier une catégorie")
    print("3. Supprimer une catégorie")
    print("4. Afficher toutes les catégories")
    print("5. Quitter")


def ajouter_categorie():
    description = input("Description : ")
    limite = float(input("Limite (€) : "))
    id_utilisateur = input("ID utilisateur : ")
    cat = CategorieDepense(description, limite, id_utilisateur)
    cat.ajouter()


def modifier_categorie():
    id_categorie = input("ID de la catégorie à modifier : ")
    nouvelle_description = input("Nouvelle description (laisser vide pour ne pas changer) : ")
    nouvelle_limite = input("Nouvelle limite (€) (laisser vide pour ne pas changer) : ")

    cat = CategorieDepense("", 0, "", id_categorie=id_categorie)
    cat.modifier(
        nouvelle_description=nouvelle_description or None,
        nouvelle_limite=float(nouvelle_limite) if nouvelle_limite else None
    )


def supprimer_categorie():
    id_categorie = input("ID de la catégorie à supprimer : ")
    cat = CategorieDepense("", 0, "", id_categorie=id_categorie)
    cat.supprimer()


def main():
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        if choix == "1":
            ajouter_categorie()
        elif choix == "2":
            modifier_categorie()
        elif choix == "3":
            supprimer_categorie()
        elif choix == "4":
            CategorieDepense.afficher_toutes()
        elif choix == "5":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide. Essayez encore.")


if __name__ == "__main__":
    main()