from models.categorie_depense import CategorieDepense
from flask import Blueprint, flash, redirect, request, render_template, url_for
from flask_login import current_user, login_required

categorie_depense_bp = Blueprint("categorie_depense", __name__)


@categorie_depense_bp.route("/categorie_depense/<string:id_categorie>")
@login_required
def afficher_categorie_depense(id_categorie):
    categorie_depense = CategorieDepense.afficher_categorie(id_categorie)
    return render_template(
        "categorie_depense.html", categorie_depense=categorie_depense
    )


@categorie_depense_bp.route("/categorie_depense", methods=["GET", "POST"])
@login_required
def ajouter_categorie_depense():
    if request.method == "POST":
        description = request.form["description"]
        limite = request.form["limite"]
        id_utilisateur = current_user.id
        if not description or not limite:
            flash("Tous les champs sont obligatoires.")
            return render_template("ajouter_categorie_depense.html")

        try:
            limite = float(request.form["limite"])
        except ValueError:
            flash("La limite doit être un nombre.")
            return render_template("ajouter_categorie_depense.html")

        categorie_depense = CategorieDepense(
            description=description, limite=limite, id_utilisateur=id_utilisateur
        )
        categorie_depense.ajouter()

        return redirect(url_for("utilisateur.profil"))
    return render_template("ajouter_categorie_depense.html")



@categorie_depense_bp.route('/supprimer_categorie_depense/<string:id_categorie>', methods=['GET', 'POST'])
@login_required
def supprimer_categorie_depense(id_categorie):
    """Cette view permet de supprimer une catégorie de dépense."""
    
    categorie_depense = CategorieDepense.afficher_categorie(id_categorie)
    if request.method == "POST":
        try:
            CategorieDepense.supprimer(id_categorie)
            return redirect(url_for("utilisateur.profil"))
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("utilisateur.profil"))
        except Exception as e:
            return redirect(url_for("utilisateur.profil"))

    return render_template(
        "suppression_confirmation_categorie_depense.html",
        categorie_depense=categorie_depense,
    )

@categorie_depense_bp.route('/modifier_categorie_depense/<string:id_categorie>', methods=['GET', 'POST'])
@login_required
def modifier_categorie_depense(id_categorie):

    categorie = CategorieDepense.afficher_categorie(id_categorie) 

    if not categorie:
        return redirect(url_for('utilisateur.profil'))

    if request.method == 'POST':
        description = request.form.get('description')
        limite = request.form.get('limite')

        try:
            limite = float(limite)
        except ValueError:
            erreur = "La limite doit être un nombre."
            return render_template("modifier_categorie_depense.html", categorie=categorie, erreur=erreur)

        updates = {"limite": limite}
        CategorieDepense.modifier(id_categorie=id_categorie, **updates)
        
        return redirect(url_for('utilisateur.profil'))
    return render_template("modifier_categorie_depense.html", categorie=categorie)