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

# Manipulação de erros da aplicação

from flask import render_template, request

def init_app(app):

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Se tentar acessar um recurso que não existe
        """
        return render_template('404.html', ip=request.environ.get('REMOTE_ADDR')), 404
   
    @app.errorhandler(500)
    def page_not_found(e):
        """
        Falha interna do servidor
        """
        return render_template('500.html', ip=request.environ.get('REMOTE_ADDR')), 500