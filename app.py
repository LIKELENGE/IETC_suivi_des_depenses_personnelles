from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.utilisateur import Utilisateur
from views.utilisateur_view import utilisateur_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.get_by_id(user_id)

app.register_blueprint(utilisateur_bp)

if __name__ == "__main__":
    app.run(debug=True)
