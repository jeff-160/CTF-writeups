<?php
	session_start();

	if ($_SERVER["REQUEST_METHOD"] === "POST") {
		if (!isset($_POST['url']))
			die('<script>alert("url inst");history.back();</script>');
		
		exec('node /bot/bot.js ' . base64_encode($_POST['url']));
		die('<script>alert("success !");history.back();</script>');
	}
?>

<form action='/bot.php' method="POST">
      URL: http://localhost/ <input type="text" name="url"><br>
	  <button>Submit</button>
</form>