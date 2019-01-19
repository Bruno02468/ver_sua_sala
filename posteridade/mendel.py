#!/bin/env python3

from urllib import request
from urllib import parse
import threading

base = "https://mendel.educacionalweb.com.br/"
urls = {
    "default": "default.asp",
    "login_do": "login_do.asp",
    "ocorrencia": "cdn_ocorrencias_visualizar.asp?id={}",
    "boletim": "boletim_mendel.asp?etapa={}&codigo={}"
}
for key, value in urls.items():
    urls[key] = base + value

def executar_login(login, senha):
    login_data = parse.urlencode({
        "url": "",
        "ac": 1,
        "eq": 1,
        "codigo": login,
        "senha": senha,
        "codescola": "MENDEL",
    }).encode("utf-8")
    login_response = request.urlopen(urls["login_do"], login_data)
    return login_response

def verificar_senha(login, senha):
    login_response = executar_login(login, senha)
    return login_response.getheader("Content-Length") == "129"

def adquirir_cookie(login, senha):
    login_response = executar_login(login, senha)
    if login_response.getheader("Content-Length") == "129":
        return "codescola=MENDEL; " + login_response.getheader("Set-Cookie")
    else:
        return None

def requisitar(pag, cookie, gets = (), data = None):
    headers = {
        "Cookie": cookie
    }
    page_request = request.Request(urls[pag].format(*gets), data, headers)
    response = request.urlopen(page_request)
    html = response.read().decode("iso-8859-1")
    return {
        "response": response,
        "html": html
    }

def _requisitar(pag, cookie, callback, gets = (), data = None):
    headers = {
        "Cookie": cookie
    }
    page_request = request.Request(urls[pag].format(gets), data, headers)
    response = request.urlopen(page_request)
    html = response.read().decode("iso-8859-1")
    callback({
        "response": response,
        "html": html
    })

def requisitar_async(*argv):
    worker = threading.Thread(target = _requisitar, args = argv)
    worker.daemon = False
    worker.start()
