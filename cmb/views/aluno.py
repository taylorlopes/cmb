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

# Gerenciamento de rotas e rotinas de Alunos

from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from cmb.plugins.database import db
from cmb.libs.models import Aluno, Turma, Perfil
from cmb.libs.forms import TurmaForm, AlunoForm
from werkzeug.datastructures import ImmutableMultiDict
from cmb.libs.util import obj2dict, get_hashed_password 
from datetime import datetime
from config import TIMEZONE
from urllib.parse import quote_plus


# Define Blueprint
aluno = Blueprint('aluno', __name__) 

@aluno.post('/alunos')
def add_aluno():
    """
    Adiciona uma aluno
    """

    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))    

    # Obtém dados do formulário
    nome = request.form['nome'].strip().upper() 
    matricula = request.form['matricula'].strip()
    id_turma = request.form['id_turma']    
    ativo = '1' if 'aluno_ativo' in request.form else '0'

    # Valida se já existe a turma
    if db.session.query(Aluno).filter_by(matricula=matricula).count() > 0:
        flash(f"Aluno com matrícula {matricula} já existe.", category='error') 
        return redirect(url_for("painel.inicial", _anchor='manutencao-alunos'))    

    # Valida os campos do formulário
    form = AlunoForm()
    form.id_turma.choices  = [(turma.id, turma.nome) for turma in Turma.query.all()]
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial", _anchor='manutencao-alunos')) 

    # Tenta adicionar os dados
    try:
        aluno = Aluno(nome=nome, matricula=matricula, id_turma=id_turma, ativo=ativo)
        db.session.add(aluno) 
        db.session.commit() 
        flash('Aluno adicionado com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao adicionar o aluno.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-alunos')) 


@aluno.post('/alunos/<matricula>/del')
def del_aluno(matricula):
    """
    Exclui uma aluno
    """ 

    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))   
        
    try:
        aluno = Aluno.query.filter_by(matricula=matricula).one()
        db.session.delete(aluno)
        db.session.commit()
        flash('Aluno excluído com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao excluir: o aluno possui vínculos.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-alunos')) 


@aluno.post('/alunos/<matricula>/edit')
def update_aluno_edit(matricula):
    """
    Atualiza aluno
    """    

    # Somente admin pode realizar esta operação
    if not Perfil.is_admin():
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))        

    # Obtém dados do formulário
    id = request.form['id'] 
    nome = request.form['nome'].strip().upper() 
    matricula = request.form['matricula'].strip() 
    id_turma = request.form['id_turma'] 
    ativo = '1' if 'aluno_ativo' in request.form else '0'


    aluno = Aluno.query.filter_by(id=id).one()

    # Valida se já existe a turma
    if matricula != aluno.matricula:
        if db.session.query(Aluno).filter_by(matricula=matricula).count() > 0:
            flash(f"Aluno com matrícula {matricula} já existe.", category='error') 
            return redirect(url_for("painel.inicial", _anchor='manutencao-alunos'))    

    # Valida os campos do formulário
    form = AlunoForm()
    form.id_turma.choices  = [(turma.id, turma.nome) for turma in Turma.query.all()]
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial", _anchor='manutencao-alunos')) 

    # Tenta atualizar os dados
    try:
        aluno.matricula = matricula
        aluno.nome = nome
        aluno.ativo = ativo
        aluno.id_turma = id_turma 
        db.session.commit() 
        flash('Aluno atualizado com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao atualizar o aluno.', category='error') 
    return redirect(url_for("painel.inicial", _anchor='manutencao-alunos')) 



@aluno.get('/alunos/matricula')
def get_aluno_matricula():
    """
    Obtém alunos com parte de matrícula (autocomplete)
    """     
    busca = f"%{request.args['matricula']}%"    
    alunos = db.session.execute(db.select(Aluno).filter(Aluno.ativo == '1', Aluno.matricula.like(busca)).order_by(Aluno.nome)).scalars().fetchall()
    suggestions = []
    for u in alunos:
        aluno = u.__dict__     
        turma = u.turma.__dict__   
        suggestions.append({
            "value": aluno['matricula'], 
            "matricula": aluno['matricula'], 
            "nome": aluno['nome'], 
            "id_turma": aluno['id_turma'],
            "turma": turma['nome']
        })
    return {"suggestions": suggestions}


@aluno.get('/alunos/nome')
def get_aluno_nome():
    """
    Obtém alunos com parte do nome (autocomplete)
    """     
    busca = f"%{request.args['aluno']}%".upper()

    alunos = db.session.execute(db.select(Aluno).filter(Aluno.ativo == '1', Aluno.nome.like(busca)).order_by(Aluno.nome)).scalars().fetchall()
    suggestions = []
    for u in alunos:
        aluno = u.__dict__     
        turma = u.turma.__dict__   
        suggestions.append({
            "value": aluno['nome'], 
            "matricula": aluno['matricula'], 
            "nome": aluno['nome'], 
            "id_turma": aluno['id_turma'],
            "turma": turma['nome']
        })
    return {"suggestions": suggestions}