<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="./static/css/font.css">
    <link rel="stylesheet" type="text/css" href="./static/css/main.css">
    <link rel="stylesheet" type="text/css" href="./static/css/login.css">
    <title>narrow site</title>
</head>
<body>
    <?php
	if(isset($_POST['username']) && isset($_POST['password'])){
	    error_reporting( E_ALL );
            ini_set( "display_errors", 1 );

	    include("config/config.php");
   	    include("config/function.php");

            $username = waf($_POST['username']);
            $password = waf($_POST['password']);
	    
	    $query = $conn->query("SELECT username FROM members WHERE username='$username' and password='$password'");
            $res = $query->fetch_all();
	    
	    if(!$res){
                    alert("Not Found User");
            }else{
                    $_SESSION['username'] = $_POST['username'];
		    location_alert("Hello User!", "/home.php");
            }
        }
    ?>
    <div class="box">
        <form method="POST">
            <div class="form">
                <h1>NARROW LOGIN</h1>
                <label>USERNAME : <input type="text" name="username"></label>
                <label>PASSWORD : <input type="password" name="password"></label>
                <input type="submit" name="submit" value="스따또~">
            </div>
        </form>
    </div>
</body>
</html>
