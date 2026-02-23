<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $_SESSION['perms'] = [];

    if ($_POST['username'] === 'admin') {
        die("Admin login is permanently disabled.");
    }

    $perm_key = $_POST['username'];
    $_SESSION['perms'][$perm_key] = 'guest_access';

    $_SESSION['username'] = $_POST['username'];
    header('location: /index.php');
    die();
}