<?php
require("db.php");
$sql = "SELECT content FROM document";
$result = $conn->query($sql);
$row = $result->fetch_assoc();
$admin_token = $row["content"];
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    include "./templates/admin.html";
}
else if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    try {
	$input_code = $_POST['access_code'];
	session_start();
        if (md5($input_code) === $admin_token && $_SERVER['REMOTE_ADDR'] === '127.0.0.1') { 
		$_SESSION['admin'] = true;
		echo "An access code has been issued upon correct access.";
		echo "Administrator privileges have been granted.";
        }
	else {
            echo "<script>alert('The access code is incorrect. Administrator registration is only possible on local host.');</script>";
            echo "<script>location.href='/index.php'</script>";
        }
    }
    catch(Exception $e) {
        echo "<script>alert('Wrong.');</script>";
        echo "<script>location.href='/index.php'</script>";
    }
}

else {
    echo "<script>alert('This is an unusual approach.');</script>";
    echo "<script>location.href='/index.php'</script>";
}
?>

