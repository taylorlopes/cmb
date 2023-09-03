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

# Adiciona filtros/funções às templates jinja

from flask import session, render_template, request
from datetime import datetime 
from config import TIMEZONE

def init_app(app):

    @app.template_filter('remove_non_numeric')    
    def remove_non_numeric(input_string):
        """
        Remove caracteres não numérico de uma string
        """        
        return ''.join(char for char in input_string if char.isnumeric())

    # Disponibiliza globalmente para as templates as funções implementadas
    app.jinja_env.globals.update(is_admin=is_admin)
    app.jinja_env.globals.update(is_gerente=is_gerente)
    app.jinja_env.globals.update(is_operador=is_operador)
    app.jinja_env.globals.update(now=now)

    
def now(format):
    """
    Retorna à template a data corrente em um formato específico
    """
    format = '%d/%m/%Y %H:%M:%s' if format == None  else format
    return datetime.now(TIMEZONE).strftime(format)

def is_admin(): 
    """
    Permite testar na template se o perfil é administrador
    """
    if 'id' in session['perfil']:   
        return True if session['perfil']['id'] == 1 else False   
    else:
        return False     
    
def is_gerente(): 
    """
    Permite testar na template se o perfil é gerente
    """    
    if 'id' in session['perfil']:   
        return True if session['perfil']['id'] == 2 else False       
    else:
        return False 
    
def is_operador(): 
    """
    Permite testar na template se o perfil é operador
    """    
    if 'id' in session['perfil']:   
        return True if session['perfil']['id'] == 3 else False      
    else:
        return False 