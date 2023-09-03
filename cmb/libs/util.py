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

# Funções genéricas e úteis à aplicação

import re
import os
import bcrypt


def obj2dict(obj):
    """
    Converte atributos do objeto/classe para dicionário (dict)

    @param object Objeto (classe Models) a ser convertido em dict
    """
    param_string = str(obj()) 
    matches = re.findall(r'\w+\((.+)\)', param_string) 
    re.sub(r'(\w+)=', r'"\1"=', matches[0])
    return eval(f"dict({matches[0]})")


def populate(el1, el2, overwrite = False): 
    """    
    Popula elemento 1 (el1) com os dados do elemnto 2 (el2)

    @param object|dict el1
    @param object|dict el2
    @param bool overwrite Se False não sobrescre el1 se el2 for None
    @return dict Sempre retorna dict e nunca alterar os objetos de entrada
    """    
    p = {}    
    e1 = el1 if el1.__class__ == dict else obj2dict(el1)
    e2 = el2 if el2.__class__ == dict else obj2dict(el2)
    for k in e1: 
        if overwrite:
            p[k] = e2[k] if k in e2 else None
        else:
            p[k] = e2[k] if k in e2 and e2[k] is not None else e1[k]
    return p


def uncapitalize(s):
    """
    Deixa a primeira letra de uma string sempre em minúscula
    """    
    return s[0].lower() + s[1:] 


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)