<?php
// programado por bruno borges paschoalinoto em 18 de dezembro de 2016
// com alterações em janeiro de 2018

$msg = "";
$f = "banco.txt";

if (isset($_POST["login"]) and isset($_POST["senha"])) {
	$login = escapeshellarg($_POST["login"]);
	$senha = escapeshellarg($_POST["senha"]);
	$cmd = escapeshellcmd("./navegante_boletim_quebrado.py $login $senha");
	$output_lines = explode("\n", shell_exec($cmd));
 	//echo("COUNT:" . count($output_lines));
	if (count($output_lines) < 3) {
		$msg = $output_lines[0];
	} else {
		$nome = $output_lines[0];
		$sala = $output_lines[1];
		$nomesala = $sala[0] . "º " . $sala[1];
		$banco = file_get_contents($f);
		if (strpos($banco, $nome) !== false) {
			$msg = "Você já está na lista, e sua sala é o $nomesala";
		} else {
			$banco .= "$nome:${sala}§";
			file_put_contents($f, $banco, LOCK_EX);
			$msg = "Você é do $nomesala, e acabamos de te colocar na lista!";
		}
	}
}

if (strlen($msg) > 0) $msg .= "<br>";

?>
<html>
	<head>
		<title>Descubra sua sala DE NOVO!</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<style>
			body {
				text-align: center;
				font-family: sans-serif;
			}
			sup {
				font-size: 50%;
			}
		</style>
	</head>
	<body onload="popularSelect()">
		<h1>Descubra sua sala!<sup>2018 edition</sup></h1>
		Você estava achando que não ia ver sua sala em 2018, né?<br>
		Errou feio! Ano novo, hack novo!<br>
		<br>
		Basta entrar com seu login (de aluno ou pais) da Sala Virtual!<br>
		<br>
		<small><i><b>Sua senha não será armazenada, e só será usada para achar sua sala.</b><br>
		Todo o código desta aplicação é
		<a target="_blank" href="//github.com/Bruno02468/ver_sua_sala/">
		aberto ao público sob uma licença livre.</a></i></small><br>
		<br>
		<form action="index.php" method="POST">
			<input type="text" name="login" placeholder="Login"><br>
			<input type="password" name="senha" placeholder="Senha"><br>
			<input type="submit" value="Bora!"><br>
		</form>
		<span id="msg"><?php echo $msg; ?></span>
		<br>
		<small><small>
		Tudo aqui foi idealizado e programado por mim, Bruno "Borginhos" Borges
		Paschoalinoto,<br>e está sob minha responsabilidade, sem associação com
		a escola ou ninguém além de mim mesmo.<br>
		</small></small>
		<br>
		Agora, para ver a lista, escolha uma sala ou ano:
		<select id="sala" oninput="listar(this.value)">
			<option value="none">- - - - -</option>
		</select><br>
		<br>
		<div id="lista"></div>
		<script>
			var banco_raw = "<?php echo file_get_contents("banco.txt"); ?>".split("§");
		</script>
		<script src="index.js"></script>
	</body>
</html>
