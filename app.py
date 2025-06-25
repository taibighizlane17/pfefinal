from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Exemple d'utilisateur fictif (في الواقع، استخدم قاعدة بيانات)
utilisateurs = {
    "admin@example.com": {
        "password": "123456",  # في الواقع، لا تخزن كلمات مرور بدون تشفير !
        "nom": "Admin"
    }
}

@app.route('/')
def accueil():
    return redirect(url_for('connexion'))

@app.route('/connexion')
def connexion():
    return render_template('connexion.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    utilisateur = utilisateurs.get(email)

    if utilisateur and utilisateur['password'] == password:
        session['email'] = email
        session['nom'] = utilisateur['nom']
        flash("Connexion réussie", "success")
        return redirect('/chat')  # interface de chat
    else:
        flash("Email ou mot de passe incorrect", "danger")
        return redirect(url_for('connexion'))

@app.route('/chat')
def chat():
    if 'email' not in session:
        return redirect(url_for('connexion'))
    return f"<h1>Bienvenue {session['nom']} dans l'espace de Chat</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('connexion'))

if __name__ == '__main__':
    app.run(debug=True)
