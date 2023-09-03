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

# Gerenciamento de rotas e rotinas de Registro de alunos

from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from cmb.plugins.database import db
from cmb.libs.models import Aluno, Turma, Registro, Perfil
from cmb.libs.forms import TurmaForm, AlunoForm, RegistroForm
from werkzeug.datastructures import ImmutableMultiDict
from cmb.libs.util import obj2dict, get_hashed_password 
import datetime 
from config import TIMEZONE
from urllib.parse import quote_plus

# Define Blueprint
registro = Blueprint('registro', __name__) 

@registro.get('/current_datetime')
def get_current_datetime(): 
    """
    Retorna a data e hora de agora
    """    
    return {'datetime': datetime.datetime.now(TIMEZONE)}

@registro.get('/today')
def get_today(): 
    """
    Retorna a data e hora de hoje, sempre començando a 0 horas (meia-noite)
    """     
    return {'datetime': datetime.now(TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0) }

@registro.post('/registros')
def add_registro():
    """
    Adiciona um registro de entrada/saída do aluno
    """

    # Somente admin e operador podem realizar esta operação
    if not (Perfil.is_admin() or Perfil.is_operador()):
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))    

    # Persiste os dados do registro na sessão e só apaga se o cadastro for com sucesso
    session['registro'].update({
        'aluno_matricula': request.form['aluno_matricula'].strip(),
        'aluno_nome': request.form['aluno_nome'].strip().upper(),
        'aluno_turma': request.form['aluno_turma'],
        'tipo_evento': request.form['tipo_evento'] if 'tipo_evento' in request.form else '',
        'dt_evento': request.form['dt_evento'] 
    })

    # return dict(session['registro'])
 

    # session['registro']['aluno_matricula'] = request.form['aluno_matricula'].strip()
    # session['registro']['aluno_nome'] = request.form['aluno_nome'].strip().upper()
    # session['registro']['aluno_turma'] = request.form['aluno_turma']
    # session['registro']['tipo_evento'] = request.form['tipo_evento']
    # session['registro']['dt_evento'] = datetime.datetime.strptime(datetime.datetime.strptime(request.form['dt_evento'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S'),  '%Y-%m-%d %H:%M:%S') 

    # Valida os campos do formulário
    form = RegistroForm()
    form.aluno_turma.choices  = [(turma.id, turma.nome) for turma in Turma.query.all()]
    if not form.validate_on_submit():
        for message in list(form.errors.values()):
            flash(message[0], category='error')
        return redirect(url_for("painel.inicial")) 
        
    # Obtém dados do formulário
    nome = request.form['aluno_nome'].strip().upper()
    matricula = request.form['aluno_matricula'].strip()
    id_turma = request.form['aluno_turma']
    tipo_evento = request.form['tipo_evento']
    dt_evento = datetime.datetime.strptime(request.form['dt_evento'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    dt_evento = datetime.datetime.strptime(dt_evento,  '%Y-%m-%d %H:%M:%S')   
    dt_lancamento = datetime.datetime.now(TIMEZONE)

    # Somente admin pode adicionar registro de qualquer data, operador só do dia corrente
    if not (Perfil.is_admin() or datetime.datetime.strftime(dt_evento, '%Y%m%d') == datetime.datetime.now(TIMEZONE).strftime('%Y%m%d')):
        flash('A data de entrada/saída deve ser de hoje.', category='error')
        return redirect(url_for("painel.inicial"))  

    try: 

        # Se aluno existir, atualiza dados do aluno
        if db.session.query(Aluno).filter_by(matricula=matricula).count() > 0:     
            aluno = Aluno.query.filter_by(matricula=matricula).one()        
            aluno.nome = nome
            aluno.id_turma = id_turma    

        # Se aluno não existir, adiciona novo aluno    
        else:                    
            aluno = Aluno(nome=nome, matricula=matricula, id_turma=id_turma)         
            db.session.add(aluno)    
            db.session.commit() # Ao fazer o commit obtém-se o id da última transação (last_id): aluno.id

        registro = Registro(id_aluno=aluno.id, id_turma=id_turma, tipo_evento=tipo_evento, dt_evento=dt_evento, dt_lancamento=dt_lancamento)
        db.session.add(registro)      
        db.session.commit() 
        Registro.reset()
        flash('Registro de entrada/saída efetuado.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao registrar entrada/saída.', category='error') 
    return redirect(url_for("painel.inicial")) 


@registro.post('/registros/<id>/del')
def del_registro(id):
    """
    Exclui um registro de entrada/saída do aluno
    """ 

    # Somente admin e operador podem realizar esta operação
    if not (Perfil.is_admin() or Perfil.is_operador()):
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))
    
    # Somente admin pode excluir registro de qualquer data, operador só do dia corrente
    registro = Registro.query.filter_by(id=id).one()
    if not (Perfil.is_admin() or registro.dt_lancamento.strftime('%Y%m%d') == datetime.datetime.now(TIMEZONE).strftime('%Y%m%d')):
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))

    try:        
        db.session.delete(registro)
        db.session.commit()
        flash('Registro excluído com sucesso.', category='success') 
    except Exception as e:
        db.session.rollback()
        db.session.flush() 
        flash('Falha ao excluir o registro.', category='error') 
    return redirect(url_for("painel.inicial"))