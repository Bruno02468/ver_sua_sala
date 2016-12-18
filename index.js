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
    for (var index in banco_raw) {
        var entry = banco_raw[index].split(":");
        var nome = entry[0];
        var sala = entry[1];
        var ano = sala[0];
        if (anos.indexOf(ano) < 0) {
            anos.push(ano);
            select.innerHTML += makeoption(ano, "Todo o " + ano + "º");
        }
        if (salas.indexOf(sala) < 0) {
            salas.push(sala);
            select.innerHTML += makeoption(sala, nomesala(sala));
            banco[sala] = [];
        }
        banco[sala].push(nome);
        banco[sala].sort();
    }
}

var lista = document.getElementById("lista");
function listar(value) {
    lista.innerHTML = "";
    if (value == "none") return false;
    for (var key in banco) {
        if (!banco.hasOwnProperty(key)) continue;
        if (key.indexOf(value) < 0) continue;
        if (value.length == 1) {
            lista.innerHTML += "<h2>" + nomesala(key) + "</h2>";
        }
        lista.innerHTML += banco[key].join("<br>") + "<br><br>";
    }
}
