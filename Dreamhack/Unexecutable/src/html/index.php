<?php
	session_start();
?>

hi .<br><br>

<?php
	$files = array_values(array_diff(scandir('.'), array('.', '..', 'files'))); 
	foreach($files as $file){
		if(is_file($file)){
			echo "<a href='/$file'>$file</a><br>"; 
		}  
	}
?>