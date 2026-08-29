<?php

	if(isset($_SESSION['username'])){
		header("location: /home.php");
	}else{
	 	header("location: /login.php");
	}

?>
<link rel="stylesheet" type="text/css" href="./static/css/font.css">
<link rel="stylesheet" type="text/css" href="./static/css/main.css">
<div style="text-align: center; font-size: 40px;">
	<?php 

		if(isset($_SESSION['username'])){
			echo "<h1>Hello ".$_SESSION['username']."</h1>";
		}

	?>
	<a href="https://www.youtube.com/watch?v=GtL1huin9EE&ab_channel=CSAAInsuranceGroup%2CaAAAInsurer">old man ( here )</a>
</div>
