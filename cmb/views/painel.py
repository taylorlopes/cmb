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

# Gerenciamento de rotas e rotinas do painel principal

from flask import Blueprint, render_template, flash, request, session, url_for, redirect
from cmb.libs.models import Perfil, Turma, Aluno, Registro
from datetime import datetime, timedelta
from config import TIMEZONE

from socket import gethostname, gethostbyname

# Define Blueprint
painel = Blueprint('painel', __name__)

@painel.get('/painel')
def inicial():
    """
    Exibe o painel principal
    """  
    
    # Verifica se o usuário está logado
    if 'login' not in session:
        return render_template('403.html', ip=request.environ.get('REMOTE_ADDR'))
    
    # Obtém os dados do painel 
    perfis = Perfil.query.all() 
    turmas = Turma.query.order_by(Turma.ativo.desc(), Turma.nome.asc()).all()
    turmas_ativas = Turma.query.filter_by(ativo="1").order_by(Turma.nome.asc()).all()
    alunos = Aluno.query.order_by(Aluno.ativo.desc(), Aluno.nome.asc()).all()    
    dt1 = request.args['dt1']+':00' if 'dt1' in request.args else datetime.now(TIMEZONE).replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
    dt2 = request.args['dt2']+':59' if 'dt2' in request.args else datetime.now(TIMEZONE).replace(hour=23, minute=59, second=59).strftime('%Y-%m-%d %H:%M:%S')
    hoje = datetime.now(TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Persiste na sessão as datas (período) da lista de entrada/saída
    if 'dt1' in request.args:
        session['dt1'] = dt1
    dt1 = session['dt1'] if 'dt1' in session else dt1       
    if 'dt2' in request.args:
        session['dt2'] = dt2
    dt2 = session['dt2'] if 'dt2' in session else dt2     

    # Limpa os campos do registro, se solicitado
    if 'reset' in request.args:
        Registro.reset()

    # Obtém os registros de alunos conforme datas do formulário
    registros = Registro.query.filter(Registro.dt_evento.between(dt1, dt2)).order_by(Registro.dt_evento.desc(), Registro.id.desc()).all()

    # Renderiza a template 
    return render_template(
        'painel.html', 
        perfis=perfis, 
        turmas=turmas, 
        turmas_ativas=turmas_ativas,        
        alunos=alunos, 
        registros=registros, 
        hoje=hoje, 
        dt1=dt1, 
        dt2=dt2
    )