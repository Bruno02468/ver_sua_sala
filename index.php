<?php

$msg = "";
$f = "banco.txt";

if (isset($_POST["login"]) and isset($_POST["senha"])) {
	$login = escapeshellarg($_POST["login"]);
	$senha = escapeshellarg($_POST["senha"]);
	$cmd = escapeshellcmd("./navegante.py $login $senha");
	$output_lines = explode("\n", shell_exec($cmd));
	if (count($output_lines) < 2) {
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
			file_put_contents($f, $banco);
			$msg = "Você é do $nomesala, e acabamos de te colocar na lista!";
		}
	}
}


?>

<html>
	<head>
		<title>Descura sua sala</title>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<style>
			body {
				text-align: center;
				font-family: sans-serif;
			}
		</style>
	</head>
	<body onload="popularSelect()">
		<h1>Descubra sua sala</h1>
		<br>
		Achar sua sala e entrar na lista é fácil.<br>
		Basta entrar com seu login e senha da Sala Virtual/Moodle.<br>
		<br>
		<form action="index.php" method="POST">
			<input type="text" name="login" placeholder="Login"><br>
			<input type="password" name="senha" placeholder="Senha"><br>
			<input type="submit" value="Bora!"><br>
		</form>
		<div id="msg"><?php echo $msg; ?></div><br>
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
