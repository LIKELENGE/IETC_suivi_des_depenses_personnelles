from flask import Blueprint, redirect, request, render_template, url_for
from flask_login import  current_user
depense_bp = Blueprint('depense_bp', __name__)


@depense_bp.route('/ajouter_depense')
def ajouter_depense():
    pass
