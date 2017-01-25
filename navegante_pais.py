#!/bin/python
# ele pega os dados necessários do site do mendel, coisa que o php não
# gosta, não vai, e não quer fazer sozinho.
# programado por bruno borges paschoalinoto em 18 de dezembro de 2016

import sys
from urllib import request
from urllib import parse
import re

def ded():
    print("Ocorreu um erro. Certifique-se de estar usando o login de pais!")
    sys.exit(0)


if len(sys.argv) < 3:
    print("Passe como argumentos o nome de usuário e senha do pai.")
    sys.exit(-1)

login = sys.argv[1]
senha = sys.argv[2]

base = "https://mendel.educacionalweb.com.br/"
login_do = base + "login_do.asp"
page_url = base + "default.asp"

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

enc = "iso-8859-1"
page_request = request.Request(page_url, None, headers)
default_response = request.urlopen(page_request)
defhtml = default_response.read().decode(enc)

boletos_link_regex = ("boletos_aluno\\.asp\\?escola=MENDEL&etapa=\\d{4}&curso="
    + "\\d{3}&serie=\d&mat=\\d{6}&turma=\\d{6}.&req=\\d&aluno=\\d{6}")

boletos_match = re.search(boletos_link_regex, defhtml)
if boletos_match == None:
    ded()

boletos_link = base + boletos_match.group()
boletos_request = request.Request(boletos_link, None, headers)
boletos_response = request.urlopen(boletos_request)
boletos_html = boletos_response.read().decode(enc)

boletos_ajax_regex = ("boletos_ajax\\.asp\\?escola=MENDEL&etapa=\d{4}"
    + "&codigo=\d{6}")
boletos_ajax_match = re.search(boletos_ajax_regex, boletos_html)
if boletos_ajax_match == None:
    ded()
boletos_ajax_link = base + boletos_ajax_match.group()
boletos_ajax_request = request.Request(boletos_ajax_link, None, headers)
boletos_ajax_response = request.urlopen(boletos_ajax_request)
boletos_ajax_html = boletos_ajax_response.read().decode(enc)

boleto_link_regex = ("boleto\\.asp\\?escola=MENDEL&matricula=\\d{6}&etapa="
    + "\\d{4}&turma=\\d{6}.&Ano=\\d{4}&Mes=\\d{2}&codbanco=\\d+&nossonumero=\\d+")
boleto_link_match = re.findall(boleto_link_regex, boletos_ajax_html)

if not boleto_link_match:
    ded()
boleto_link = base + boleto_link_match[-1]

boleto_request = request.Request(boleto_link, None, headers)
boleto_response = request.urlopen(boleto_request)
boleto_html = boleto_response.read().decode(enc)

salareg = ("Aluno:\\d{6} - (.+) \\(Mensalidade - \\d{2}\\/\\d{4}\\)-(\\d)ª série (.)")
match = re.search(salareg, boleto_html)
if match == None:
    ded()
nome = match.group(1)
sala = match.group(2) + match.group(3)

if not sala or not nome:
    ded()

print(nome)
print(sala)
