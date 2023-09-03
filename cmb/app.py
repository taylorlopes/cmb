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

# Aplicação para registrar o controle de entrada e saída de alunos  

from flask import Flask 
from cmb.plugins import configs
from cmb.plugins import csrf
from cmb.plugins import database
from cmb.plugins import errors
from cmb.plugins import jinja
from cmb.views.auth import auth
from cmb.views.painel import painel
from cmb.views.perfil import perfil
from cmb.views.turma import turma
from cmb.views.aluno import aluno
from cmb.views.registro import registro
 
def create_app():
    app = Flask(__name__)
    configs.init_app(app)  
    csrf.init_app(app)  
    database.init_app(app)  
    errors.init_app(app)  
    jinja.init_app(app)  
    app.register_blueprint(auth)
    app.register_blueprint(painel)
    app.register_blueprint(perfil)
    app.register_blueprint(turma)
    app.register_blueprint(aluno)
    app.register_blueprint(registro)    
    return app 