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

# Gerenciamento de rotas e rotinas de Ano/Turmas

from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from cmb.plugins.database import db
from cmb.libs.models import Turma, Perfil
from cmb.libs.forms import TurmaForm
from werkzeug.datastructures import ImmutableMultiDict
from cmb.libs.util import get_hashed_password 
from datetime import datetime
from config import TIMEZONE

# Define Blueprint
turma = Blueprint('turma', __name__)


@turma.post('/turmas')
def add_turma():
    """
    Adiciona uma turma
    """    

    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))       

    # Torna compatível nome de campos que vem do formulário com validador libs.forms.py
    dataform = request.form.to_dict()  
    dataform['nome'] = request.form['turma']
    request.form = ImmutableMultiDict(dataform)

    # Obtém dados do formulário
    nome = request.form['nome'] 
    ativo = '1' if 'turma_ativo' in request.form else '0'

    # Valida se já existe a turma
    if db.session.query(Turma).filter_by(nome=nome).count() > 0:
        flash(f"Falha ao adicionar. Turma {nome} já existe.", category='error') 
        return redirect(url_for("painel.inicial", _anchor='manutencao-turmas'))    

    # Valida os campos do formulário
    form = TurmaForm()
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial", _anchor='manutencao-turmas')) 
 
    # Tenta adicionar os dados
    try:
        turma = Turma(nome=nome, ativo=ativo)
        db.session.add(turma) 
        db.session.commit() 
        flash('Turma adicionada com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao adicionar a turma.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-turmas')) 


@turma.post('/turmas/<id>/del')
def del_turma(id):
    """
    Exclui uma turma
    """    
    
    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))   
    
    try:
        turma = Turma.query.filter_by(id=id).one()
        db.session.delete(turma)
        db.session.commit()
        flash('Turma excluída com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao excluir: a turma possui vínculos.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-turmas')) 



@turma.post('/turmas/<id>/edit')
def update_turma_edit(id):
    """
    Atualiza turma
    """     

    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))       
 
    # Torna compatível nome de campos que vem do formulário com validador libs.forms.py
    dataform = request.form.to_dict()  
    dataform['nome'] = request.form['turma']
    request.form = ImmutableMultiDict(dataform)     

    # Obtém dados do formulário
    id = request.form['id'] 
    nome = request.form['nome'].strip() 
    ativo = '1' if 'turma_ativo' in request.form else '0'
    
    turma = Turma.query.filter_by(id=id).one() 

    # Valida os campos do formulário
    form = TurmaForm() 
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial", _anchor='manutencao-turmas')) 

    # Tenta atualizar os dados
    try:        
        turma.nome = nome
        turma.ativo = ativo
        db.session.commit() 
        flash('Turma atualizada com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao atualizar a turma.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-turmas')) 
