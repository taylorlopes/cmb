"""
Copyright (c) CMB/EB 2023, All Rights Reserved 

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED 
IN THIS NOTICE BE LIABLE FOR ANY CLAIM OR CONSEQUENTIAL DAMAGES OR ANY 
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING
OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Author Taylor Lopes <taylor.lopes@eb.mil.br>
""" 

# Gerenciamento de rotas e rotinas de Autenticação (Auth)

from flask import Blueprint, current_app, render_template, flash, request, session, url_for, redirect
from cmb.plugins.database import db 
from cmb.libs.models import Perfil, Registro
from cmb.libs.forms import PerfilForm
from cmb.libs.util import populate 
from datetime import datetime 
from config import TIMEZONE
from cmb.libs.util import check_password
 

# Define Blueprint
auth = Blueprint('auth', __name__)


@auth.get('/')
@auth.get('/login')
def login():    
    """
    Exibe tela de login
    """   
    
    if 'login' not in session:
        session['perfil'] = {"nome": session['perfil']['nome']} if "perfil" in session else {"nome": ""}     
        perfis = Perfil.query.all()        
        return render_template('login.html', perfis=perfis)
    else:
        return redirect(url_for("painel.inicial"))

 
@auth.get('/logout')
def logout():     
    """
    Efetua o logout
    """       
    session.clear()
    return redirect(url_for("auth.login"))   


@auth.post('/autenticar')
def autenticar(): 
    """
    Autenticação do usuário
    """
    id = request.form['id']
    senha = request.form['senha'] 

    # Valida os campos do formulário
    form = PerfilForm()
    form.id.choices  = [(perfil.id, perfil.nome) for perfil in Perfil.query.all()]
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("auth.login")) 
 
    # Busca o perfil e compara a senha
    perfil = Perfil.query.filter_by(id=id).first()

    # Se usuário autenticado com falha
    if not check_password(senha, perfil.senha):
        flash('Perfil e senha não conferem.', category='error')
        return redirect(url_for("auth.login"))    

    # Inicializa dados do registro persistidos na sessão
    Registro.reset()

    # Se usuário autenticado com sucesso
    session['login']  = True
    perfil.senha = None
    session['perfil'] = perfil.as_dict()
    return redirect(url_for("painel.inicial"))