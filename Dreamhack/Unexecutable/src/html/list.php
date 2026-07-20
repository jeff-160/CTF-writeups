<?php
	session_start();
?>
My File List<br><br>
<?php
	if (isset($_SESSION['path'])) {
		$path = $_SESSION['path'];
		$files = array_values(array_diff(scandir("files/$path"), array('.', '..'))); 
		foreach($files as $file)
			echo "<a href='/files/$path/$file'>$file</a><br>"; 
	}
?>