#!/bin/python
# ele pega os dados necessários do site do mendel, coisa que o php não
# gosta, não vai, e não quer fazer sozinho.
# programado por bruno borges paschoalinoto em 18 de dezembro de 2016

import sys
from urllib import request
from urllib import parse
import re

if len(sys.argv) < 3:
    print("Passe como argumentos o nome de usuário e senha.")
    sys.exit(-1)

login = sys.argv[1]
senha = sys.argv[2]

login_do = "https://mendel.educacionalweb.com.br/login_do.asp"
page_url = "https://mendel.educacionalweb.com.br/default.asp"

login_data = parse.urlencode({
    "url": "",
    "ac": 1,
    "eq": 1,
    "codigo": login,
    "senha": senha,
    "codescola": "MENDEL",
}).encode("utf-8")

login_response = request.urlopen(login_do, login_data)

if login_response.getheader("Content-Length") != "129":
    print("As credenciais inseridas não são válidas!")
    sys.exit(-1)

headers = {
    "Cookie": login_response.getheader("Set-Cookie")
}

page_request = request.Request(page_url, None, headers)

default_response = request.urlopen(page_request)
html = default_response.read().decode("iso-8859-1")

nome_regex = ("<td align=\"right\" style=\"padding-top:20px;\">\r\n"
    " {20}<b>([^<]+)")
nome = re.search(nome_regex, html).group(1)

sala_regex = ("mostra_boletim\.asp\?escola=MENDEL&etapa=.{4}&curso=.{3}&serie="
    ".&mat=.{6}&turma=.{5}(.{2})")
sala = re.search(sala_regex, html).group(1)

if not sala or not nome:
    print("Ocorreu um erro ao ler o HTML da sua página. Avise o Bruno.")
    sys.exit(0)

print(nome)
print(sala)
