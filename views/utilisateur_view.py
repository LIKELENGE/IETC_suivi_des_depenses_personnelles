from flask import flash
from models.utilisateur import Utilisateur
from datetime import datetime
from flask import Blueprint, redirect,request, render_template, url_for
from flask_login import login_user, current_user, login_required,logout_user
from models.categorie_depense import CategorieDepense
from models.statistique_financiere import StatistiqueFinanciere

utilisateur_bp = Blueprint("utilisateur", __name__)

@utilisateur_bp.route("/", methods=["GET", "POST"])
#Route principale (accueil + connexion)
def accueil():
    if current_user.is_authenticated:
        return redirect(url_for("utilisateur.profil"))
    if request.method == "POST":
        email = request.form.get("email")
        mot_de_passe = request.form.get("mot_de_passe")
        utilisateur = Utilisateur.se_connecter(email,mot_de_passe)
        if utilisateur is None:
            flash("Email ou mot de passe invalides.")
            return render_template("index.html")
        else:
            login_user(utilisateur)
            return redirect(url_for("utilisateur.profil"))
    return render_template("index.html")

@utilisateur_bp.route("/profil", methods=["GET", "POST"])
@login_required
def profil():
    """Route pour afficher le profil de l'utilisateur"""
    utilisateur = {
        "id_utilisateur": current_user.id_utilisateur,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "email": current_user.email,
    }

    now = datetime.now()
    mois_courant = now.month
    annee_courante = now.year

    if request.method == "POST":
        mois_courant = int(request.form["mois"])
        annee_courante = int(request.form["annee"])
        
    statistique_financiere = StatistiqueFinanciere(mois_courant, annee_courante)
    solde = statistique_financiere.solde()
    revenus = statistique_financiere.revenus
    depenses = statistique_financiere.depenses
    solde_par_categorie = statistique_financiere.solde_par_categorie()
    return render_template(
        "profil.html",
        utilisateur=utilisateur,
        mois_courant=mois_courant,
        annee_courante=annee_courante,
        revenus=revenus, 
        depenses=depenses,
        solde=solde,
        solde_par_categorie=solde_par_categorie,
        
    )
    

@utilisateur_bp.route("/inscription", methods=["GET", "POST"])
def inscription():
    """Route pour l'inscription
    Récupération des champs du formulaire
    Vérifie si les mots de passe correspondent
    Création d’un nouvel utilisateur"""
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        mot_de_passe_confirmation = request.form["mot_de_passe_confirmation"]
        if mot_de_passe != mot_de_passe_confirmation:
            flash("Les mots de passe ne correspondent pas.")
            return render_template("inscription.html")
        nouvel_utilisateur = Utilisateur(nom, prenom, email, mot_de_passe)
        try:    
            resultat = nouvel_utilisateur.ajouter()
        except ValueError as e:
            flash(str(e))
            return render_template("inscription.html")
        if resultat == 0:
            flash("Email déjà utilisé.")
            return render_template("inscription.html")
        login_user(nouvel_utilisateur)
        return redirect(url_for("utilisateur.profil"))
    return render_template("inscription.html")


@utilisateur_bp.route("/modification", methods=["GET", "POST"])
@login_required
def modification():
    """Route pour modifier les informations de l'utilisateur"""
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"].strip()
        mot_de_passe_confirmation = request.form["mot_de_passe_confirmation"].strip()
        if mot_de_passe:
            if mot_de_passe != mot_de_passe_confirmation:
                flash("Les mots de passe ne correspondent pas.")
                return render_template("modification.html", utilisateur=current_user)
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
    """Route pour supprimer le compte utilisateur"""
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
    """Route pour se déconnecter"""
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("utilisateur.accueil"))


@utilisateur_bp.route("/export_csv", endpoint="export_csv")
@login_required
def export_csv():
    """Route pour exporter les statistiques en CSV"""
    mois = request.args.get('mois', type=int)
    annee = request.args.get('annee', type=int)
    stats = StatistiqueFinanciere(mois, annee)
    return stats.generer_csv()

@utilisateur_bp.route("/export_pdf", endpoint="export_pdf")
@login_required
def export_pdf():
    """Route pour exporter les statistiques en PDF"""
    mois = request.args.get('mois', type=int)
    annee = request.args.get('annee', type=int)
    stats = StatistiqueFinanciere(mois, annee)
    return stats.generer_pdf()

@utilisateur_bp.route("/options-avancees")
@login_required
def options_avancees():
    """Route pour afficher les options avancées"""
    return render_template("options_avancees.html")
