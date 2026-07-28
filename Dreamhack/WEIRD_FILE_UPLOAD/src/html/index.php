<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weird File Upload</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');
        
        body {
            font-family: 'Creepster', cursive;
            background-color: #000000;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ff6600' fill-opacity='0.1' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E");
        }
        .container {
            width: 80%;
            max-width: 600px;
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border: 3px solid #ff6600;
            box-shadow: 0 0 15px #ff6600, inset 0 0 15px #ff6600;
            animation: pulsate 2s infinite alternate;
        }
        @keyframes pulsate {
            0% { box-shadow: 0 0 15px #ff6600, inset 0 0 15px #ff6600; }
            100% { box-shadow: 0 0 25px #ff00ff, inset 0 0 25px #ff00ff; }
        }
        h1 {
            color: #39ff14;
            text-align: center;
            font-size: 3em;
            text-shadow: 2px 2px #ff6600, -2px -2px #ff00ff;
            margin-bottom: 30px;
            letter-spacing: 3px;
        }
        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
            margin-bottom: 10px;
        }
        .file-input-wrapper input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
        }
        .file-input-wrapper .btn {
            background-color: #000;
            color: #39ff14;
            border: 2px solid #39ff14;
            padding: 8px 20px;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            display: inline-block;
            width: 100%;
            box-sizing: border-box;
            text-align: center;
            font-family: 'Creepster', cursive;
        }
        .submit-btn {
            background-color: #ff6600;
            color: #000;
            border: none;
            padding: 10px 20px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            display: block;
            width: 100%;
            margin-top: 10px;
            font-family: 'Creepster', cursive;
            letter-spacing: 2px;
            text-shadow: 1px 1px #ff00ff;
        }
        .submit-btn:hover {
            background-color: #39ff14;
            color: #000;
            text-shadow: 1px 1px #ff6600;
        }
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            font-size: 18px;
            text-align: center;
        }
        .success {
            background-color: #39ff14;
            color: #000;
            border: 2px solid #ff6600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>WEIRD FILE UPLOAD</h1>
        <form action="" method="post" enctype="multipart/form-data">
            <div class="file-input-wrapper">
                <button class="btn" type="button">Choose Your Anomaly</button>
                <input type="file" name="file" required>
            </div>
            <input type="submit" value="UPLOAD TO THE UNKNOWN" class="submit-btn">
        </form>

        <?php
        $seedFile = "/seed.txt";
        $uploadDir = "./uploads/";
        $maxFileSize = 10000; 

        $seed = file_get_contents($seedFile);
        mt_srand($seed);
        $randomValue = mt_rand();

        function displayMessage($message) {
            echo "<div class='message success'>$message</div>";
        }

        if ($_SERVER['REQUEST_METHOD'] == "POST") {
            if (!empty($_FILES["file"]["name"]) && $_FILES["file"]["size"] <= $maxFileSize && strpos($_FILES["file"]["name"], "..") === false) {
                $ip = $_SERVER['REMOTE_ADDR'];
                $hash = hash('sha256', $randomValue . $ip);
                $newFilename = $hash . "_" . basename($_FILES["file"]["name"]);
                $uploadFile = $uploadDir . $newFilename;

                if (move_uploaded_file($_FILES["file"]["tmp_name"], $uploadFile)) {
                    displayMessage("Your cosmic anomaly has been absorbed into our bizarre dimension!");
                }
            }
        } elseif (isset($_GET["try"])) {
            $path = "./uploads/" . $_GET["try"];
            if (strpos($path, "..") === false) {
                include $path;
            }
        }
        ?>
    </div>
    <script>
        document.querySelector('input[type="file"]').addEventListener('change', function(e){
            let fileName = e.target.files[0] ? e.target.files[0].name : "No Reality Distortion Detected";
            this.previousElementSibling.textContent = fileName;
        });
    </script>
</body>
</html>