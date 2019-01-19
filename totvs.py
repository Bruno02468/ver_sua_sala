#!/bin/env python3

# baseado em mendel.py, na pasta "posteridade", adptado para o sistema da TOTVS

# bibliotecas para fazer requests
from urllib import request
from urllib import parse
# biblioteca de regexes
import re

# hosts para onde fazemos requisições
host1 = "saea.totvscloud.com.br"
host2 = "saea.totvscloud.com.br:8082"

# urls-base dos hosts, o urllib chora se a gente não colocar https://
base1 = "https://" + host1
base2 = "https://" + host2

# user agent falso
ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ("
    "KHTML, like Gecko) Chrome/73.0.3642.0 Safari/537.36")

# urls dos diversos serviços que vamos utilizar
urls = {
    "login": base1 + ("/Corpore.Net/Source/EDU-EDUCACIONAL/Public/"
        "EduPortalAlunoLogin.aspx?AutoLoginType=ExternalLogin&undefined"),
    "dados": base2 + "/RM/API/TOTVSEducacional/Aluno/DadosPessoais",
    "portal":  base2 + "/web/app/edu/PortalEducacional/",
    "loginpage": base2 + "web/app/edu/PortalEducacional/login/"
}

# faz o login para obter um cookie de sessão, para podermos executar requisições
# que exigem estar logado como um aluno
def executar_login(login, senha):
    login_data = parse.urlencode({
        "User": login,
        "Pass": senha,
        "Alias": "CorporeRM"
    }).encode("utf-8")
    login_headers = {
        "Cookie": ("cookie_balance=365958316.37407.0000; "
            "EduContextoAlunoResponavelAPI=; DefaultAlias=CorporeRM;"),
        "Host": host1,
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Origin": host2,
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9;q=0.8",
        "Referer": urls["loginpage"],
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    login_request = request.Request()
    login_response = request.urlopen(urls["login"], login_data)
    result = {
        "obj": login_response,
        "data": login_response.read().decode("utf-8"),
    }
    result["success"] = "Usuário ou Senha inválidos" not in result["data"]
    return result

# requisita uma página que requer login de aluno, exige um cookie obtido como
# acima.
def requisitar(urlname, cookie, inserts = (), data = None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "DNT": "1",
        "Host": host1,
        "Pragma": "no-cache",
        "Referer": urls["portal"],
        "User-Agent": ua
    }
    if ("8082" in urls[urlname]):
        headers["Host"] = host2
    page_request = request.Request(urls[urlname].format(inserts), data, headers)
    print(page_request.header_items())
    response = request.urlopen(page_request)
    data = response.read().decode("utf-8")
    return {
        "obj": response,
        "data": data
    }
