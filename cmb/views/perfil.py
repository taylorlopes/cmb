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

# Gerenciamento de rotas e rotinas do Perfil de usuário

from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from cmb.plugins.database import db
from cmb.libs.models import Perfil
from cmb.libs.forms import PerfilForm
from werkzeug.datastructures import ImmutableMultiDict
from cmb.libs.util import get_hashed_password 
from datetime import datetime
from config import TIMEZONE

# Define Blueprint
perfil = Blueprint('perfil', __name__)


@perfil.post('/perfis/edit')
def update_id_perfil():
    """
    Atualiza perfil baseado no id
    """    

    # Torna compatível nome de campos que vem do formulário com validador libs.forms.py
    dataform = request.form.to_dict()  
    dataform['id'] = request.form['id_perfil']
    request.form = ImmutableMultiDict(dataform)

    # Obtém dados do formulário
    id = request.form['id']
    senha = request.form['senha'] 

    # Valida os campos do formulário
    form = PerfilForm()
    form.id.choices  = [(perfil.id, perfil.nome) for perfil in Perfil.query.all()]
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial", _anchor='manutencao-senhas')) 
 
    # Tenta atualizar os dados
    try:
        perfil = db.session.execute(db.select(Perfil).filter_by(id=id)).scalar_one()
        perfil.senha = senha=get_hashed_password(request.form['senha']) 
        db.session.commit()
        flash('Senha atualizada com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao atualizar a senha.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-senhas')) 
