from datetime import datetime
from flask import Blueprint, redirect,request, render_template, url_for
from models.utilisateur import Utilisateur
from flask_login import login_user, current_user, login_required
utilisateur_bp = Blueprint("utilisateur", __name__)


@utilisateur_bp.route("/", methods=["GET", "POST"])
def accueil():
    if current_user.is_authenticated:
        return redirect(url_for("utilisateur.profil"))
    if request.method == "POST":
        email = request.form.get("email")
        mot_de_passe = request.form.get("mot_de_passe")
        utilisateur = Utilisateur.se_connecter(email,mot_de_passe)
        if utilisateur is None:
            return render_template("index.html", error="email ou mot de passe invalides")
        else:
            login_user(utilisateur)
            return redirect(url_for("utilisateur.profil"))
    return render_template("index.html")

@utilisateur_bp.route("/profil")
@login_required
def profil():

    utilisateur = {
        "id_utilisateur": current_user.id_utilisateur,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "email": current_user.email
    }
    mois_courant = datetime.now().month
    annee_courante = datetime.now().year 
    return render_template("profil.html", utilisateur=utilisateur, mois_courant=mois_courant, annee_courante=annee_courante)



# @utilisateur_bp.route("/inscription/", methods=["GET", "POST"])
# def inscription():
#     if request.method == "POST":
#         nom = request.form["nom"]
#         prenom = request.form["prenom"]
#         email = request.form["email"]
#         mot_de_passe = request.form["mot_de_passe"]
#         utilisateur = Utilisateur.ajouter()
#         if any(u["email"] == email for u in utilisateur):
#             return "Email déjà utilisé", 409
#         nouvel_utilisateur = Utilisateur(nom, prenom, email, mot_de_passe)
#         nouvel_utilisateur.ajouter()
#         return redirect(url_for("utilisateur.accueil"))
#     return render_template("inscription.html")