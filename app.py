from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.utilisateur import Utilisateur

app = Flask(__name__)
app.secret_key = "super-secret-key"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        utilisateurs = gestionnaire.lire()
        if any(u["email"] == email for u in utilisateurs):
            return "Email déjà utilisé", 409
        nouvel_utilisateur = Utilisateur(nom, prenom, email, mot_de_passe)
        nouvel_utilisateur.ajouter()
        return redirect(url_for("login"))
    return '''
        <h2>Créer un compte</h2>
        <form method="post">
            Nom: <input name="nom"><br>
            Prénom: <input name="prenom"><br>
            Email: <input name="email"><br>
            Mot de passe: <input type="password" name="mot_de_passe"><br>
            <input type="submit" value="S'inscrire">
        </form>
    '''

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        user = Utilisateur.se_connecter(email, mot_de_passe)
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Identifiants invalides", 401
    return '''
        <h2>Connexion</h2>
        <form method="post">
            Email: <input name="email"><br>
            Mot de passe: <input type="password" name="mot_de_passe"><br>
            <input type="submit" value="Se connecter">
        </form>
        <p>Pas encore inscrit ? <a href="/register">Créer un compte</a></p>
    '''

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Bienvenue {current_user.prenom} ! <a href='/logout'>Se déconnecter</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
