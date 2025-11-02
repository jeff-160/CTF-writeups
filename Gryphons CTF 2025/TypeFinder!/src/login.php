<?php

session_start();
$users_file = '/var/private/users.json';
$users = json_decode(file_get_contents($users_file), true);

$user = $_POST['user'] ?? '';
$pass = $_POST['pass'] ?? '';

if (!isset($users[$user])) {
    echo "Invalid username :(<br><a href='index.php'>Back</a>";
    exit;
}

$stored = $users[$user]['password'] ?? '';

if (md5($pass) == $stored) {
    $_SESSION['user'] = $user;
    header("Location: admin.php");
    exit;
} else {
    echo "Wrong password :(<br><a href='index.php'>Back</a>";
    exit;
}