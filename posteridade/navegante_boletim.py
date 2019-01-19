#!/bin/python

import mendel
import sys
import datetime
from urllib.error import HTTPError
import re

if len(sys.argv) != 3:
    print("Especifique usuário e senha!")
    sys.exit(0)

login = sys.argv[1]
senha = sys.argv[2]
ano_atual = datetime.datetime.now().year
cookie = mendel.adquirir_cookie(login, senha)

if not cookie:
    print("Suas credenciais não são válidas! :(")
    sys.exit(0)

default_html = mendel.requisitar("default", cookie)["html"]
try:
    boletim_html = mendel.requisitar("boletim", cookie, (ano_atual, login))["html"]
except HTTPError as error:
    boletim_html = error.read().decode("iso-8859-1")

nome_rx = r"<b>([^<]+)</b>"
sala_rx = r"TURMA: (\d)(?:º|ª) (?:série|ano) (.)"
match_nome = re.search(nome_rx, boletim_html)
match_sala = re.search(sala_rx, boletim_html)
if not match_nome or not match_sala:
    print("Algo deu MUITO errado. Notifique o Bruno. Imediatamente.")
    sys.exit(0)

nome = match_nome.group(1)
sala = match_sala.group(1) + match_sala.group(2)

print(nome + "\n" + sala)
