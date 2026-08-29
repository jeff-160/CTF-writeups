<?php 

include("config/config.php");
include("config/function.php");

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="./static/css/font.css">
    <link rel="stylesheet" type="text/css" href="./static/css/main.css">
    <link rel="stylesheet" type="text/css" href="./static/css/table.css">
    <title>NARROW HOME</title>
</head>
<body>
    <div>
        <h1>Members Lookup</h1>
    </div>
    <table>
        <thead>
            <tr>
                <td>USER</td>
                <td>Email</td>
                <td>Comment</td>
                <td>REGISTER DATE</td>
            </tr>
        </thead>
        <?php

            if(isset($_GET['username']) && isset($_GET['email'])){

                $username = waf($_GET['username']);
                $email = waf($_GET['email'], true);

                $query = $conn->query("SELECT * FROM members WHERE username='$username' and email='$email'");
                $res = $query->fetch_assoc();
		if(!$res){
			alert("Not Found :(");
		}else{
			?>
                    	<tr>
                        	<td><?php echo $res['username']; ?></td>
                        	<td><?php echo $res['email']; ?></td>
                        	<td><?php echo $res['comment']; ?></td>
                        	<td><?php echo $res['regdate']; ?></td>
                    	</tr>
                <?php
		}
            }else{

                $query = $conn->query("SELECT * FROM members");

		while($res = mysqli_fetch_assoc($query)){
				
                    if($res['role'] == 'admin'){
                    	?>

				<tr>
					<td colspan=4>** NO PERMISSION **</td>
				</tr>

			<?php
                    }else{

                        ?>
    
                        <tr>
                            <td><?php echo $res['username']; ?></td>
                            <td><?php echo $res['email']; ?></td>
                            <td><?php echo $res['comment']; ?></td>
                            <td><?php echo $res['regdate']; ?></td>
                        </tr>
    
                        <?php
                    } 
                }
            }

        ?>
    </table>
</body>
</html>
