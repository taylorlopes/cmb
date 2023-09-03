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

# Validação de formulários com Flask WTF
# Documentação: https://flask-wtf.readthedocs.io/en/1.0.x/quickstart/

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, ValidationError, DateField
from wtforms.validators import InputRequired, DataRequired, Length 
from validate_docbr import CPF
import re
 

class PerfilForm(FlaskForm):
    id = SelectField(
                choices=[],
                coerce=int,
                validators=[DataRequired(message="Selecione uma opção válida para perfil.")]
            )
    senha = StringField(
                    validators=[InputRequired(message="A senha é obrigatória."),
                    Length(min=8, max=8, message="A senha deve possuir 8 dígitos.")]
                )
    

class TurmaForm(FlaskForm):
    nome = StringField(
                    validators=[InputRequired(message="O nome da turma é obrigatório."),
                    Length(min=2, max=50, message="O nome da turma deve ter de 2 a 50 caracteres.")]
                )
      

class AlunoForm(FlaskForm):
    id_turma = SelectField(
                choices=[],
                coerce=int, 
                validators=[DataRequired(message="Selecione uma opção válida para turma.")]
            )
    nome = StringField(
                    validators=[InputRequired(message="O nome do aluno é obrigatório."),
                    Length(min=3, max=100, message="O nome do aluno deve ter de 3 a 80 caracteres.")
                    ]
                )
    matricula = StringField(
                    validators=[InputRequired(message="A matrícula é obrigatória."),
                    Length(min=2, max=50, message="A matrícula deve ter de 2 a 50 caracteres.")
                    ]
                )    
    
class RegistroForm(FlaskForm):
 
    aluno_turma = SelectField(
                choices=[],
                coerce=int, 
                validators=[DataRequired(message="Selecione uma opção válida para turma.")]
            )
    
    aluno_matricula = StringField(
                    validators=[InputRequired(message="A matrícula é obrigatória."),
                    Length(min=2, max=50, message="A matrícula deve ter de 2 a 50 caracteres.")
                    ]
                ) 
                
    aluno_nome = StringField(
                    validators=[InputRequired(message="O nome do aluno é obrigatório."),
                    Length(min=3, max=100, message="O nome do aluno deve ter de 3 a 80 caracteres.")
                    ]
                )
    
    tipo_evento = SelectField(
                choices=[1, 2],
                coerce=int, 
                validators=[DataRequired(message="Selecione opção entrada ou saída.")]
            )

    dt_evento = DateField(
                    format='%d/%m/%Y %H:%M', 
                    validators=[DataRequired(message="A data de entrada/saída é obrigatória")]
                ) 