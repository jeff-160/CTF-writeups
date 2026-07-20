<?php
	session_start();
	
	function check_valid($str) {
		$len = strlen($str);
		for ($i = 0; $i < $len; $i++) {
			if (strpos("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", $str[$i]) === false)
				return False;
		}
		
		return True;
	};

	if ($_SERVER["REQUEST_METHOD"] === "POST") {
		$name = $_POST['name_name name'];
		$filter = $_POST['filter_filter_filter'];
		
		if (!isset($name) || !isset($filter) || gettype($name) !== "string" || gettype($filter) !== "string")
			die('<script>alert("name or filter isnt");history.back();</script>');
		
		if (!check_valid($name) || strlen($name) > 10)
			die('<script>alert("invalid name");history.back();</script>');
		$name .= '.png';
		
		if (strlen($filter) > 1200 || strpos($filter, '.') !== false || strpos($filter, '/') !== false || strpos(strtolower($filter), '%2e') !== false || strpos(strtolower($filter), '%2f') !== false)
			die('<script>alert("invalid filter");history.back();</script>');
		$img = file_get_contents("php://filter/$filter/resource=basedpng.txt");
		
		if (strpos($img, 'resource') !== false)
			die('<script>alert("invalid filter");history.back();</script>');
		$img = base64_decode($img);
		
		if (!isset($_SESSION['path']))
			$_SESSION['path'] = bin2hex(random_bytes(20));
		$path = "files/" . $_SESSION['path'];
		
		if (!is_dir($path))
			mkdir($path);
		
		file_put_contents("$path/$name", $img);
		die('<script>alert("success !");history.back();</script>');
	}
?>
<form action='/upload.php' method="POST">
      Image Name: <input type="text" name="name_name name"><br>
      Filter: <input type="text" name="filter_filter_filter"><br>
	  <button>Submit</button>
</form>