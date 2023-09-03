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

# Criar tabelas e inserts inicial da aplicação (sqlite3) e reseta passwords

"""
- Para apagar todo o banco de dados, execute:
docker exec -it cmb python db-create.py --reset

- Para apagar todas as senhas (Senha padrão: 12345678), execute: 
docker exec -it cmb python db-create.py --pwd

"""

from cmb.plugins.database import db
from cmb.app import create_app
import argparse 
from cmb.libs.util import get_hashed_password 
from cmb.libs.models import Perfil
 

# Criar DB primeira vez
app = create_app()
with app.app_context():    
    
    # Obtém argumentos da linha de comando
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help', help='Mostra esta ajuda.')
    parser.add_argument('-r', '--reset', action='store_true', help='Apaga todos os dados da aplicação.')
    parser.add_argument('-p', '--pwd', action='store_true', help='Redefine todas as senhas da aplicação.')
    args = parser.parse_args()

    # Exige ao menos um parâmetro/argumento
    if not (args.reset or args.pwd):
        print(f'Execute {parser.prog} --reset para apagar todos os dados da aplicação.')
        print(f'Execute {parser.prog} --pwd para redefinir todas as senhas da aplicação.')
        print(f'Execute {parser.prog} --help para ajuda.')
        quit() 

    # Apaga as tabelas criadas em cmb.libs.models
    if args.reset:        
        db.drop_all() 
        db.create_all()
        print('Banco de dados criado com sucesso!')
        print('Senha padrão: 12345678')        

    # Redefine tabela perfil (senhas) em cmb.libs.models
    if args.pwd:        
        Perfil.__table__.drop(db.engine)
        Perfil.__table__.create(db.engine)
        print('Senhas redefinidas com sucesso!')
        print('Senha padrão: 12345678')  

    # Inserts inicial
    db.session.add(Perfil(id=1, nome='Administrador', descricao='Permissão para realizar manutenção geral de dados.', senha=get_hashed_password('12345678')))
    db.session.add(Perfil(id=2, nome='Gerente', descricao='Permissão para visualizar registros de entrada e saída de alunos.', senha=get_hashed_password('12345678')))
    db.session.add(Perfil(id=3, nome='Operador', descricao='Permissão para cadastrar entrada e saída de alunos.', senha=get_hashed_password('12345678')))
    db.session.commit()

