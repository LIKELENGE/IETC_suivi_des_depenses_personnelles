from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models.depense import Depense
from models.categorie_depense import CategorieDepense
import datetime

depense_bp = Blueprint('depense', __name__)


@depense_bp.route('/ajouter_depense', methods=['GET', 'POST'])
@login_required
def ajouter_depense():
    utilisateur_id = current_user.id
    now = datetime.datetime.now()
    mois = int(request.values.get('mois', now.month))
    annee = int(request.values.get('annee', now.year))
    categories = CategorieDepense.lister_categorie_par_personne(utilisateur_id)

    if request.method == 'POST':
        montant = float(request.form['montant'])
        date_transaction = request.form['date_transaction']
        heure_transaction = request.form['heure_transaction']
        libelle = request.form['libelle']
        deductible_fiscalement = request.form.get('deductible_fiscalement') == 'True'
        id_categorie = request.form['id_categorie']

        quota_restant = Depense.verifier_limite(utilisateur_id, mois, annee, id_categorie)

        if montant > quota_restant:
            return render_template('ajouter_depense.html',
                                   categories=categories,
                                   mois=mois,
                                   annee=annee,
                                   quota_restant=quota_restant,
                                   selected_id_categorie=id_categorie,
                                   erreur='Votre quota est insuffisant.')

        depense = Depense(utilisateur_id, montant, date_transaction, heure_transaction, id_categorie, libelle, deductible_fiscalement)
        depense.ajouter()

        return redirect(url_for("utilisateur.profil"))

    elif request.method == 'GET' and 'id_categorie' in request.args:

        id_categorie = request.args['id_categorie']
        quota_restant = Depense.verifier_limite(utilisateur_id, mois, annee, id_categorie)

        return render_template('ajouter_depense.html',
                               categories=categories,
                               mois=mois,
                               annee=annee,
                               quota_restant=quota_restant,
                               selected_id_categorie=id_categorie)

    return render_template('ajouter_depense.html', categories=categories, mois=mois, annee=annee)





@depense_bp.route('/modifier_depense/<string:id_transaction>', methods=['GET', 'POST'])       
@login_required
def modifier_depense(id_transaction):
    depenses = Depense.depenses_par_utilisateur(current_user.id)
    depense = next((d for d in depenses if d.id_transaction == id_transaction), None)
    
    if not depense:
        flash("Dépense introuvable.", "error")
        return redirect(url_for('utilisateur.profil'))
    if request.method == 'POST':
        montant = float(request.form['montant'])
        date_transaction = request.form['date_transaction']
        heure_transaction = request.form['heure_transaction']
        libelle = request.form['libelle']
        deductible_fiscalement = request.form.get('deductible_fiscalement') == 'True'
        Depense.modifier(id_transaction, montant=montant, date_transaction=date_transaction, heure_transaction=heure_transaction, libelle=libelle, deductible_fiscalement=deductible_fiscalement)
        flash("Dépense modifiée avec succès.", "success")
        return redirect(url_for('utilisateur.profil'))
    categorie_depense=CategorieDepense.afficher_categorie(depense.categorie)
    return render_template('modifier_depense.html', depense=depense, categorie_depense=categorie_depense)

    

@depense_bp.route('/depenses_supprimer/<id_transaction>', methods=['POST'])
@login_required
def supprimer_depense(id_transaction):
    Depense.supprimer(id_transaction)
    flash("Dépense supprimé.", "info")
    return redirect(url_for('utilisateur.profil'))