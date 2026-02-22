<?php
    error_reporting(0);
    $content = $_POST['content'];
    $file = $_GET['file'];

    if (isset($file) && isset($content)) {
        
        $exit = '<?php exit(); ?>';
        $blacklist = ['base64', 'rot13', 'string.strip_tags'];

        foreach($blacklist as $b){
            if(stripos($file, $b) !== false){
                die('Hacker!!!');
            }
        }

        file_put_contents($file, $exit . $content);
	
	usleep(50000);

        echo 'file written: ' . $file;
    }

    highlight_file(__FILE__);
?>
