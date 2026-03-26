<?php
require("db.php");
ini_set('phar.readonly',0);
class Requests {
    public $url;
    private $options;
    private $postData;
    private $cookie;
    function __construct($url, $postData = '', $cookie = '', $options = array()) {
        $this->url = $url;
        $this->postData = $postData;
        $this->cookie = $cookie;
        $this->options = $options;
    }

    function __destruct(){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        if (!empty($this->postData)) {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $this->postData);
        }

        if (!empty($this->cookie)) {
            curl_setopt($ch, CURLOPT_COOKIE, $this->cookie);
        }

        foreach ($this->options as $option => $value) {
            curl_setopt($ch, $option, $value);
        }

        $output = curl_exec($ch);
        echo $output;
        curl_close($ch);
    }
}
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        include "./templates/delete.html";

    }
    else {
        if($_POST['title']) {
            $title = $_POST['title'];
            if (strpos($title, '..') !== false) {
                echo "Filtered.";
                exit(-1);
            }

            $filePath = $title;
            $imageType = pathinfo($filePath, PATHINFO_EXTENSION);
	    $allowedTypes = ['png', 'jpg', 'jpeg'];
	    if (!in_array(strtolower($imageType), $allowedTypes)) {
    		echo "Invalid image type.";
    		exit(-1);
	    }
	    $imageData = file_get_contents($filePath);
	    if ($imageData == null) {
		$filePath = './uploads/' . $filePath;
		$imageData = file_get_contents($filePath);
	    }
            $base64 = 'data:image/' . $imageType . ';base64,' . base64_encode($imageData);
            include "./templates/delete_real.html";
            echo '<img src="' . $base64 . '" alt="Deleted Image File">';
            try {
                $stmt = $conn->prepare("DELETE FROM document where filename=?");
                $stmt->bind_param('s', $title);
                $stmt->execute();
                $valid_filename_pattern = '/^[a-zA-Z0-9_.-]+$/';

                if (preg_match($valid_filename_pattern, $title)) {
                    system("rm -rf ./uploads/" . escapeshellarg($title));
                } else {
                    echo "Invalid file name.";
                    echo '</div>
                  </body>
                  </html>';
                    exit(-1);
                }
                echo "Success Deleted!";
                echo '</div>
                  </body>
                  </html>';
            } catch (mysqli_sql_exception $e) {
                echo "Query failed: " . $e->getMessage();
            }

        }
        else {
            echo "<script>alert('Error. Please Contact admin.');</script>";
            echo "<script>location.href='/index.php'</script>";
        }
    }
?>


