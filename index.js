// programado por bruno borges paschoalinoto em 18 de dezembro de 2016

banco_raw = banco_raw.slice(0, -1);
var anos = [];
var salas = [];
var banco = {};

function nomesala(str) {
    return str[0] + "º " + str[1];
}

function makeoption(value, text) {
    return "<option value=\"" + value + "\">" + text + "</option>";
}


var select = document.getElementById("sala");
function popularSelect() {
    var selects = [];
    for (var index in banco_raw) {
        var entry = banco_raw[index].split(":");
        var nome = entry[0];
        var sala = entry[1];
        var ano = sala[0];
        if (selects.indexOf(ano) < 0) {
            selects.push(ano);
        }
        if (selects.indexOf(sala) < 0) {
            selects.push(sala);
            banco[sala] = [];
        }
        banco[sala].push(nome);
    }
    selects.sort();
    for (var index in selects) {
        var s = selects[index];
        if (s.length == 1) {
            select.innerHTML += makeoption(s, "Todo o " + s + "º");
        } else {
            select.innerHTML += makeoption(s, nomesala(s));
        }
    }
}

var lista = document.getElementById("lista");
function listar(value) {
    lista.innerHTML = "";
    if (value == "none") return false;
    var keyd = [];
    for (var key in banco) {
        if (!banco.hasOwnProperty(key)) continue;
        keyd.push(key);
    }
    keyd.sort();
    for (var i in keyd) {
        var key = keyd[i];
        if (key.indexOf(value) < 0) continue;
        lista.innerHTML += "<h2>" + nomesala(key) + "</h2>";
        lista.innerHTML += banco[key].join("<br>") + "<br><br>";
    }
}
