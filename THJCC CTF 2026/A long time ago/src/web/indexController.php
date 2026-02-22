<?php
session_start();

$flag = "THJCC{FAKE_FLAG}";

if(!isset($_SESSION['username'])){
    header('location: /login.php');
}

$is_admin = false;
if (isset($_SESSION['perms'])) {
    foreach ($_SESSION['perms'] as $key => $value) {
        if ($key == 'admin') { 
            $is_admin = true;
            break;
        }
    }
}

$username_display = htmlspecialchars($_SESSION['username']);
