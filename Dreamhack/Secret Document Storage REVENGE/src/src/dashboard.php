<?php
require("db.php");
session_start();

if ($_SESSION['admin']) {
    if ($_POST['filename']) {
        $filename = strtolower($_POST['filename']);

        if (strpos($filename, "uploads") !== false) {
            echo "<div class='center-text'>Access to this file is restricted.</div>";
        } else {
            include "./templates/dashboard.html";
            include ($filename);
        }
    }
    else {
        include "./templates/dashboard.html";
    }
}
else {
    echo "<div class='center-text'>You are not admin.</div>";
}
?>

