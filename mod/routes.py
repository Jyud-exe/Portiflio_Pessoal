from mod import app
from flask import render_template, redirect, url_for, request, flash
from mod.forms import cadForm, loginForm, feedForms
from flask_login import login_user, current_user, logout_user
import sqlite3

@app.route('/', methods=['GET', 'POST'])
def home():
    form = loginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('home', id=None))
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS comentarios (id INTEGER PRIMARY KEY AUTOINCREMENT, mensagem TEXT NOT NULL, user TEXT, user_id INTEGER)')
        cursor.execute('SELECT user, mensagem FROM comentarios ORDER BY id DESC LIMIT 2') 
        comentarios = cursor.fetchall()
        print(comentarios)
    return render_template('index.html', form=form, comentarios=comentarios)


@app.route('/cadastro', methods=['GET', 'POST'])
def cad():
    form = cadForm() 
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('cadastro.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/salvar', methods=['POST'])
def salvar():

    form = request.form.get('feedback', '').strip()
    if not form:
        flash('Comentario vazio não pode ser enviado.')
        return redirect(url_for('home'))
    user = current_user.nome
    user_id = current_user.id
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comentarios (mensagem, user, user_id) VALUES (?, ?, ?)', (form, user, user_id))
        conn.commit()
        return redirect(url_for('home'))

    
   
    