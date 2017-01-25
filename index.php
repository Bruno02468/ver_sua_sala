<?php
// programado por bruno borges paschoalinoto em 18 de dezembro de 2016

$msg = "";
$f = "banco.txt";

if (isset($_POST["login"]) and isset($_POST["senha"])) {
	$login = escapeshellarg($_POST["login"]);
	$senha = escapeshellarg($_POST["senha"]);
	$cmd = escapeshellcmd("./navegante_pais.py $login $senha");
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
		<title>Descubra sua sala!</title>
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
		<h1>Descubra sua sala!</h1>
		<br>
		O esquema que eu descobri ano passado para achar sua sala foi legal.<br>
		Mas isto aqui é melhor. Nada de digitar listas na mão.<br>
		Basta entrar com seu login e senha <b>DE PAIS</b> da Sala Virtual.<br>
		<br>
		<u>Este método dos boletos não funciona para quem pagou anuidade, e
		para bolsistas. Desculpe.</u><br>
		<br>
		<i><b>Sua senha não será armazenada, e só será usada para achar sua sala.</b><br>
		Todo o código desta aplicação é
		<a target="_blank" href="//github.com/Bruno02468/ver_sua_sala/">
		aberto ao público sob uma licença livre.</a></i><br>
		<br>
		Tudo aqui foi idealizado e programado por mim, Bruno Borges Paschoalinoto.<br>
		<br>
		<form action="index.php" method="POST">
			<input type="text" name="login" placeholder="Login"><br>
			<input type="password" name="senha" placeholder="Senha"><br>
			<input type="submit" value="Bora!"><br>
		</form>
		<span id="msg"><?php echo $msg; ?></span>
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
