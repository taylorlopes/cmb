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

# Models - Mapeamento entre classes e banco de dados (ORM)

from flask import render_template, request, session
from sqlalchemy.inspection import inspect
from sqlalchemy import ForeignKeyConstraint
from cmb.plugins.database import db
from datetime import datetime 
from dataclasses import dataclass 
from config import TIMEZONE


class TimestampModel(db.Model):
    """
    Permite outras classes Model herdar datas de criação e atualização
    """
    __abstract__ = True
    dt_criado = db.Column(db.DateTime, nullable=False, default=datetime.now(TIMEZONE))
    dt_atualizado = db.Column(db.DateTime, default=datetime.now(TIMEZONE), onupdate=datetime.now(TIMEZONE))


@dataclass
class Perfil(db.Model):   
    """
    Model Perfil
    """
    __tablename__ = 'perfil'
    __bind_key__ = "sqlite"
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nome:str = db.Column(db.String(100), unique=True, nullable=False) 
    descricao:str = db.Column(db.String(100), unique=True, nullable=False) 
    senha:str = db.Column(db.String(100), unique=False, nullable=False) 

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)    
        
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }    
    
    def is_admin():
        return True if session['perfil']['id'] == 1 else False   
    def is_gerente():
        return True if session['perfil']['id'] == 2 else False   
    def is_operador():
        return True if session['perfil']['id'] == 3 else False   
    
@dataclass
class Turma(db.Model):   
    """
    Model Turma
    """
    __tablename__ = 'turma'
    __bind_key__ = "sqlite"
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome:str = db.Column(db.String(100), unique=True, nullable=False)
    ativo:str = db.Column(db.String(1), unique=False, nullable=False, default="1")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)    
        
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }    
    

@dataclass
class Aluno(db.Model):
    """
    Model Aluno
    """
    __tablename__ = 'aluno'
    __bind_key__ = "sqlite"
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_turma:int = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False) 
    nome:str = db.Column(db.String(100), nullable=False)
    matricula:str = db.Column(db.String(10), unique=True, nullable=False)
    turma = db.relationship('Turma', primaryjoin='Aluno.id_turma == Turma.id', foreign_keys=[id_turma], viewonly=True)
    ativo:str = db.Column(db.String(1), unique=False, nullable=False, default="1")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)    
        
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

@dataclass
class Registro(TimestampModel, db.Model):
    """
    Model Registro (Entrada/Saída)
    """
    __tablename__ = 'registro'
    __bind_key__ = "sqlite"
    id:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno:int = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False) 
    id_turma:int = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False) 
    dt_lancamento:datetime = db.Column(db.DateTime, nullable=False, default=datetime.now(TIMEZONE))  
    tipo_evento:str = db.Column(db.String(1), unique=False, nullable=True)
    dt_evento:datetime = db.Column(db.DateTime, nullable=False, default=datetime.now(TIMEZONE))  
    aluno = db.relationship('Aluno', primaryjoin='Registro.id_aluno == Aluno.id', foreign_keys=[id_aluno], viewonly=True)
    turma = db.relationship('Turma', primaryjoin='Registro.id_turma == Turma.id', foreign_keys=[id_turma], viewonly=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)    
        
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        } 

    def reset():
        """
        Inicializa dados do registro persistidos na sessão
        """
        session['registro'] =  {
            'aluno_matricula': '',
            'aluno_nome': '',
            'aluno_turma': '',
            'tipo_evento': '',
            'dt_evento': ''
        }             