from models.utilisateur import Utilisateur
from datetime import datetime
from flask import Blueprint, redirect,request, render_template, url_for
from flask_login import login_user, current_user, login_required,logout_user
from models.categorie_depense import CategorieDepense

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
    categories_depenses = CategorieDepense.lister_categorie_par_personne(current_user.id_utilisateur)
   
    utilisateur = {
        "id_utilisateur": current_user.id_utilisateur,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "email": current_user.email
    }
    mois_courant = datetime.now().month
    annee_courante = datetime.now().year 
    return render_template("profil.html", utilisateur=utilisateur,
                            mois_courant=mois_courant, 
                            annee_courante=annee_courante,
                            categories_depenses=categories_depenses)

@utilisateur_bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    erreur = None
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        mot_de_passe_confirmation = request.form["mot_de_passe_confirmation"]
        if mot_de_passe != mot_de_passe_confirmation:
            return render_template(
                "inscription.html", erreur="Les mots de passe ne correspondent pas"
            )
        nouvel_utilisateur = Utilisateur(nom, prenom, email, mot_de_passe)
        resultat = nouvel_utilisateur.ajouter()
        if resultat == 0:
            return render_template("inscription.html", erreur="Email déjà utilisé")
        login_user(nouvel_utilisateur)
        return redirect(url_for("utilisateur.profil"))
    return render_template("inscription.html", erreur=erreur)


@utilisateur_bp.route("/modification", methods=["GET", "POST"])
@login_required
def modification():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"].strip()
        mot_de_passe_confirmation = request.form["mot_de_passe_confirmation"].strip()
        if mot_de_passe:
            if mot_de_passe != mot_de_passe_confirmation:
                erreur = "Les mots de passe ne correspondent pas."
                return render_template("modification.html", utilisateur=current_user, erreur=erreur)
        try:
            updates = {"nom": nom,"prenom": prenom,"email": email,}
            if mot_de_passe:
                updates["mot_de_passe"] = mot_de_passe
            Utilisateur.modifier(current_user.id_utilisateur, **updates)
        except ValueError as e:
            return render_template("modification.html", utilisateur=current_user, erreur=str(e))
        return redirect(url_for("utilisateur.profil"))
    return render_template("modification.html", utilisateur=current_user)

@utilisateur_bp.route("/suppression", methods=["GET", "POST"])
@login_required
def suppression():
    if request.method == "POST":
        try:
            Utilisateur.supprimer(current_user.id_utilisateur)
            logout_user()
            return redirect(url_for("utilisateur.accueil"))
        except ValueError as e:
            return render_template("index.html", utilisateur=current_user, erreur=str(e))

    return render_template("suppression_confirmation.html", utilisateur=current_user)


@utilisateur_bp.route("/deconnexion")
def deconnexion():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("utilisateur.accueil"))



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