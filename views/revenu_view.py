from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.revenu import Revenu
from datetime import datetime


revenu_bp = Blueprint("revenu_bp", __name__)


@revenu_bp.route("/ajouter_revenu", methods=["GET", "POST"])
@login_required
def ajouter_revenu():
    """Route pour ajouter un revenu."""
    if request.method == "POST":
        montant_str = request.form["montant"]
        date_transaction = request.form.get("date")
        heure_transaction = request.form.get("heure")
        libelle = request.form["libelle"]
        imposable = "imposable" in request.form
        try:
            montant = float(montant_str)
            if montant <= 0:
                raise ValueError
        except (ValueError, TypeError):
            flash("Le montant doit être un nombre positif.", "error")
            return render_template("ajouter_revenu.html")

        if not date_transaction or not date_transaction.strip():
            date_transaction = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date_transaction, "%Y-%m-%d")
            except ValueError:
                flash("La date doit être au format AAAA-MM-JJ.", "error")
                return render_template("ajouter_revenu.html")

        if not heure_transaction or not heure_transaction.strip():
            heure_transaction = datetime.now().strftime("%H:%M")
        else:
            try:
                datetime.strptime(heure_transaction, "%H:%M")
            except ValueError:
                flash("L'heure doit être au format HH:MM.", "error")
                return render_template("ajouter_revenu.html")

        if not libelle or not libelle.strip():
            flash("Le libellé est obligatoire.", "error")
            return render_template("ajouter_revenu.html")

        revenu = Revenu(
            utilisateur_id=current_user.id,
            montant=montant,
            date_transaction=date_transaction,
            heure_transaction=heure_transaction,
            libelle=libelle,
            imposable=imposable,
        )
        revenu.ajouter()
        flash("Revenu ajouté avec succès.", "success")
        return redirect(url_for("utilisateur.profil"))

    return render_template("ajouter_revenu.html")





@revenu_bp.route("/revenus/supprimer/<id_transaction>", methods=["POST"])
@login_required
def supprimer_revenu(id_transaction):
    """Route pour supprimer un revenu."""
    Revenu.supprimer(id_transaction)
    flash("Revenu supprimé.", "info")
    return redirect(url_for("utilisateur.profil"))
