from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.revenu import Revenu
from datetime import datetime


revenu_bp = Blueprint('revenu_bp', __name__)

@revenu_bp.route('/ajouter_revenu', methods=['GET', 'POST'])
@login_required
def ajouter_revenu():
    if request.method == 'POST':
        montant = request.form['montant']
        date_transaction = request.form['date']
        libelle = request.form['libelle']
        imposable = 'imposable' in request.form
        heure_transaction = datetime.now().strftime('%H:%M')

        if not libelle.strip():
            flash("Le libellé est obligatoire.", "error")
            return render_template('ajouter_revenu.html')

        revenu = Revenu(
            utilisateur_id=current_user.id,
            montant=float(montant),
            date_transaction=date_transaction,
            heure_transaction=heure_transaction,
            libelle=libelle,
            imposable=imposable
        )
        revenu.ajouter()
        flash("Revenu ajouté avec succès.", "success")
        return redirect(url_for('revenu_bp.lister_revenus'))

    return render_template('ajouter_revenu.html')



@revenu_bp.route('/revenus')
@login_required
def lister_revenus():
    revenus = Revenu.revenue_par_utilisateur(current_user.id)
    return  redirect(url_for('utilisateur.profil'))



@revenu_bp.route('/modifier_revenu/<id_transaction>', methods=['GET', 'POST'])
@login_required
def modifier_revenu(id_transaction):
    revenus = Revenu.revenue_par_utilisateur(current_user.id)
    revenu = next((r for r in revenus if r.id_transaction == id_transaction), None)
    
    if not revenu:
        flash("Revenu introuvable.", "error")
        return redirect(url_for('revenu_bp.lister_revenus'))

    if request.method == 'POST':
        montant = request.form['montant']
        date = request.form['date']
        libelle = request.form['libelle']
        imposable = 'imposable' in request.form

        if not libelle.strip():
            flash("Le libellé est obligatoire.", "error")
            return render_template('modifier_revenu.html', revenu=revenu)

        Revenu.modifier(
            id_transaction,
            montant=float(montant),
            date_transaction=date,
            libelle=libelle,
            imposable=imposable
        )
        flash("Revenu modifié avec succès.", "success")
        return redirect(url_for('utilisateur.profil'))

    return render_template('modifier_revenu.html', revenu=revenu)



@revenu_bp.route('/revenus/supprimer/<id_transaction>', methods=['POST'])
@login_required
def supprimer_revenu(id_transaction):
    Revenu.supprimer(id_transaction)
    flash("Revenu supprimé.", "info")
    return redirect(url_for('uitilisateur.profil'))
