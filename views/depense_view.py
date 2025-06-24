from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models.depense import Depense
from models.categorie_depense import CategorieDepense
import datetime

depense_bp = Blueprint("depense", __name__)


@depense_bp.route("/ajouter_depense", methods=["GET", "POST"])
@login_required
def ajouter_depense():
    """Route pour ajouter une dépense."""
    utilisateur_id = current_user.id
    now = datetime.datetime.now()
    mois = int(request.values.get("mois", now.month))
    annee = int(request.values.get("annee", now.year))
    categories = CategorieDepense.lister_categorie_par_personne(utilisateur_id)

    if request.method == "POST":
        montant_str = request.form.get("montant")
        date_transaction = request.form.get("date_transaction")
        heure_transaction = request.form.get("heure_transaction")
        libelle = request.form.get("libelle")
        id_categorie = request.form.get("id_categorie")
        deductible_fiscalement = request.form.get("deductible_fiscalement") == "True"

        try:
            montant = float(montant_str)
            if montant <= 0:
                raise ValueError
        except (ValueError, TypeError):
            erreur = "Le montant doit être un nombre positif."
            return render_template(
                "ajouter_depense.html",
                categories=categories,
                mois=mois,
                annee=annee,
                erreur=erreur,
            )

        if not date_transaction or not date_transaction.strip():
            date_transaction = now.strftime("%Y-%m-%d")
        else:
            try:
                datetime.datetime.strptime(date_transaction, "%Y-%m-%d")
            except ValueError:
                erreur = "La date doit être au format AAAA-MM-JJ."
                return render_template(
                    "ajouter_depense.html",
                    categories=categories,
                    mois=mois,
                    annee=annee,
                    erreur=erreur,
                )

        if not heure_transaction or not heure_transaction.strip():
            heure_transaction = now.strftime("%H:%M")
        else:
            try:
                datetime.datetime.strptime(heure_transaction, "%H:%M")
            except ValueError:
                erreur = "L'heure doit être au format HH:MM."
                return render_template(
                    "ajouter_depense.html",
                    categories=categories,
                    mois=mois,
                    annee=annee,
                    erreur=erreur,
                )

        if not libelle or not libelle.strip():
            erreur = "Le libellé est obligatoire."
            return render_template(
                "ajouter_depense.html",
                categories=categories,
                mois=mois,
                annee=annee,
                erreur=erreur,
            )

        if not id_categorie:
            erreur = "Veuillez choisir une catégorie."
            return render_template(
                "ajouter_depense.html",
                categories=categories,
                mois=mois,
                annee=annee,
                erreur=erreur,
            )

        quota_restant = Depense.verifier_limite(
            utilisateur_id, mois, annee, id_categorie
        )

        if montant > quota_restant:
            erreur = "Votre quota est insuffisant."
            return render_template(
                "ajouter_depense.html",
                categories=categories,
                mois=mois,
                annee=annee,
                quota_restant=quota_restant,
                selected_id_categorie=id_categorie,
                erreur=erreur,
            )

        depense = Depense(
            utilisateur_id,
            montant,
            date_transaction,
            heure_transaction,
            id_categorie,
            libelle,
            deductible_fiscalement,
        )
        depense.ajouter()

        flash("Dépense ajoutée avec succès.", "success")
        return redirect(url_for("utilisateur.profil"))

    elif request.method == "GET" and "id_categorie" in request.args:
        id_categorie = request.args["id_categorie"]
        quota_restant = Depense.verifier_limite(
            utilisateur_id, mois, annee, id_categorie
        )

        return render_template(
            "ajouter_depense.html",
            categories=categories,
            mois=mois,
            annee=annee,
            quota_restant=quota_restant,
            selected_id_categorie=id_categorie,
        )

    return render_template(
        "ajouter_depense.html", categories=categories, mois=mois, annee=annee
    )


@depense_bp.route("/depenses_supprimer/<id_transaction>", methods=["POST"])
@login_required
def supprimer_depense(id_transaction):
    """Route pour supprimer une dépense."""
    Depense.supprimer(id_transaction)
    flash("Dépense supprimée.")
    return redirect(url_for("utilisateur.profil"))
