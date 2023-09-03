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

# Inicializa instância do banco de dados com respectivas configurações

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = binds()["sqlite"]
    app.config['SQLALCHEMY_BINDS'] = binds() 
    app.config['SQLALCHEMY_ECHO'] = False
    db.init_app(app)   

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Habilita o uso de foreign key para o sqlite
    https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close() 


def sqlite(): 
    """
    String de conexão com o banco de dados Sqlite
    """    
    connection_string = 'sqlite:////app/db/cmb.db'
    return connection_string
 

def binds():   
    """
    Mapeia a conexão a ser utilizada pelo ORM SqlAlchemy em Models
    """       
    SQLALCHEMY_BINDS = {
        "sqlite":     sqlite(),
 
    }
    return SQLALCHEMY_BINDS